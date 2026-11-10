"""
🍎 Apple Store India — Full-Featured FastAPI E-Commerce Application
===================================================================
Backend: FastAPI + PyMySQL + Jinja2 Templates
Database: MySQL 8.x (apple_store)
Features: Product catalog, user auth, cart, wishlist, coupons/discounts,
          orders, reviews, admin dashboard, search, category filtering.

Run: uvicorn main:app --reload --port 8000
"""

import os
import json
import math
import re
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Request, Form, Query, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from database import get_db, get_cursor
from auth import hash_password, verify_password, generate_session_token, generate_order_number
from models import (
    UserRegister, UserLogin, CartAdd, CartUpdate,
    CouponApply, OrderCreate, ReviewCreate, AddressCreate
)


# ─── App Initialization ──────────────────────────────────────

app = FastAPI(title="Apple Store India", version="2.0.0")

# Session middleware for cookie-based user sessions
app.add_middleware(
    SessionMiddleware,
    secret_key="apple_store_super_secret_key_2026_india_manit",
    session_cookie="apple_session",
    max_age=86400 * 7,  # 7 days
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Mount static files and templates
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


# ─── Template Helpers & Context ───────────────────────────────

def format_price(value) -> str:
    """Format a number as Indian Rupee string: ₹1,19,900."""
    if value is None:
        return "₹0"
    value = float(value)
    if value < 0:
        return f"-₹{format_price(-value)[1:]}"
    integer_part = int(value)
    decimal_part = round(value - integer_part, 2)

    s = str(integer_part)
    if len(s) <= 3:
        formatted = s
    else:
        last_three = s[-3:]
        remaining = s[:-3]
        # Group remaining digits in pairs from the right
        groups = []
        while remaining:
            groups.append(remaining[-2:])
            remaining = remaining[:-2]
        groups.reverse()
        formatted = ",".join(groups) + "," + last_three

    if decimal_part > 0:
        return f"₹{formatted}.{str(decimal_part).split('.')[1][:2]}"
    return f"₹{formatted}"


# Register custom Jinja2 filter
templates.env.filters["inr"] = format_price
templates.env.globals["now"] = datetime.now


def get_user(request: Request) -> Optional[dict]:
    """Extract current user from session."""
    return request.session.get("user")


def get_cart_count(request: Request) -> int:
    """Get the number of items in the user's cart."""
    user = get_user(request)
    if not user:
        return 0
    with get_db() as conn:
        cur = get_cursor(conn)
        cur.execute("SELECT COALESCE(SUM(quantity), 0) AS cnt FROM cart_items WHERE user_id = %s", (user["user_id"],))
        row = cur.fetchone()
        return int(row["cnt"]) if row else 0


def get_wishlist_count(request: Request) -> int:
    """Get the number of items in the user's wishlist."""
    user = get_user(request)
    if not user:
        return 0
    with get_db() as conn:
        cur = get_cursor(conn)
        cur.execute("SELECT COUNT(*) AS cnt FROM wishlist WHERE user_id = %s", (user["user_id"],))
        row = cur.fetchone()
        return int(row["cnt"]) if row else 0


def base_context(request: Request) -> dict:
    """Common template context variables injected into every page."""
    messages = request.session.pop("messages", []) if "messages" in request.session else []
    return {
        "request": request,
        "user": get_user(request),
        "cart_count": get_cart_count(request),
        "wishlist_count": get_wishlist_count(request),
        "messages": messages,
    }


def flash(request: Request, text: str, msg_type: str = "info"):
    """Add a flash message to the session."""
    if "messages" not in request.session:
        request.session["messages"] = []
    request.session["messages"].append({"type": msg_type, "text": text})


def require_login(request: Request) -> dict:
    """Returns user dict or raises redirect."""
    user = get_user(request)
    if not user:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    return user


def require_admin(request: Request) -> dict:
    """Returns admin user dict or raises 403."""
    user = get_user(request)
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


# ─── Page Routes ──────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    """Landing page with featured products and categories."""
    ctx = base_context(request)
    with get_db() as conn:
        cur = get_cursor(conn)

        # Featured products
        cur.execute("""
            SELECT p.*, c.category_name, c.icon AS category_icon
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE p.is_featured = TRUE AND p.is_active = TRUE
            ORDER BY p.created_at DESC LIMIT 8
        """)
        ctx["featured_products"] = cur.fetchall()

        # Categories
        cur.execute("""
            SELECT c.*, COUNT(p.product_id) AS product_count
            FROM categories c
            LEFT JOIN products p ON c.category_id = p.category_id AND p.is_active = TRUE
            GROUP BY c.category_id
            ORDER BY c.display_order
        """)
        ctx["categories"] = cur.fetchall()

    return templates.TemplateResponse(request=request, name="index.html", context=ctx)


@app.get("/products", response_class=HTMLResponse)
async def products_page(
    request: Request,
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = "newest",
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    page: int = 1,
):
    """Product listing with filtering, search, and sorting."""
    ctx = base_context(request)
    per_page = 12

    with get_db() as conn:
        cur = get_cursor(conn)

        # Build query dynamically
        where_clauses = ["p.is_active = TRUE"]
        params = []

        if category:
            where_clauses.append("c.category_name = %s")
            params.append(category)

        if search:
            where_clauses.append("(p.product_name LIKE %s OR p.description LIKE %s)")
            params.extend([f"%{search}%", f"%{search}%"])

        if min_price is not None:
            where_clauses.append("p.price >= %s")
            params.append(min_price)

        if max_price is not None:
            where_clauses.append("p.price <= %s")
            params.append(max_price)

        where_sql = " AND ".join(where_clauses)

        # Sort
        sort_map = {
            "price_asc": "p.price ASC",
            "price_desc": "p.price DESC",
            "newest": "p.created_at DESC",
            "rating": "p.rating_avg DESC",
            "name": "p.product_name ASC",
        }
        order_sql = sort_map.get(sort, "p.created_at DESC")

        # Count total
        cur.execute(f"""
            SELECT COUNT(*) AS total
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE {where_sql}
        """, params)
        total = cur.fetchone()["total"]
        total_pages = max(1, math.ceil(total / per_page))
        offset = (page - 1) * per_page

        # Fetch products
        cur.execute(f"""
            SELECT p.*, c.category_name, c.icon AS category_icon
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE {where_sql}
            ORDER BY {order_sql}
            LIMIT %s OFFSET %s
        """, params + [per_page, offset])
        ctx["products"] = cur.fetchall()

        # Categories for filter sidebar
        cur.execute("""
            SELECT c.*, COUNT(p.product_id) AS product_count
            FROM categories c
            LEFT JOIN products p ON c.category_id = p.category_id AND p.is_active = TRUE
            GROUP BY c.category_id
            ORDER BY c.display_order
        """)
        ctx["categories"] = cur.fetchall()

    ctx["current_category"] = category
    ctx["search_query"] = search
    ctx["current_sort"] = sort
    ctx["min_price"] = min_price
    ctx["max_price"] = max_price
    ctx["page"] = page
    ctx["total_pages"] = total_pages
    ctx["total_products"] = total

    return templates.TemplateResponse(request=request, name="products.html", context=ctx)


@app.get("/product/{slug}", response_class=HTMLResponse)
async def product_detail_page(request: Request, slug: str):
    """Single product detail view."""
    ctx = base_context(request)

    with get_db() as conn:
        cur = get_cursor(conn)

        cur.execute("""
            SELECT p.*, c.category_name, c.icon AS category_icon
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE p.slug = %s AND p.is_active = TRUE
        """, (slug,))
        product = cur.fetchone()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Parse specs JSON
        if product.get("specs") and isinstance(product["specs"], str):
            try:
                product["specs"] = json.loads(product["specs"])
            except json.JSONDecodeError:
                product["specs"] = {}

        # Fetch reviews
        cur.execute("""
            SELECT r.*, u.full_name
            FROM reviews r
            JOIN users u ON r.user_id = u.user_id
            WHERE r.product_id = %s
            ORDER BY r.created_at DESC
        """, (product["product_id"],))
        ctx["reviews"] = cur.fetchall()

        # Related products (same category, exclude current)
        cur.execute("""
            SELECT p.*, c.category_name, c.icon AS category_icon
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE p.category_id = %s AND p.product_id != %s AND p.is_active = TRUE
            ORDER BY RAND() LIMIT 4
        """, (product["category_id"], product["product_id"]))
        ctx["related_products"] = cur.fetchall()

        # Check if user has this in wishlist
        user = get_user(request)
        ctx["in_wishlist"] = False
        if user:
            cur.execute("SELECT 1 FROM wishlist WHERE user_id = %s AND product_id = %s",
                        (user["user_id"], product["product_id"]))
            ctx["in_wishlist"] = cur.fetchone() is not None

    ctx["product"] = product
    return templates.TemplateResponse(request=request, name="product_detail.html", context=ctx)


@app.get("/cart", response_class=HTMLResponse)
async def cart_page(request: Request):
    """Shopping cart page."""
    ctx = base_context(request)
    user = get_user(request)

    if not user:
        flash(request, "Please sign in to view your bag.", "warning")
        return RedirectResponse("/login", status_code=303)

    with get_db() as conn:
        cur = get_cursor(conn)
        cur.execute("""
            SELECT ci.*, p.product_name, p.price, p.mrp, p.slug, p.stock_quantity,
                   p.image_url, c.icon AS category_icon, c.category_name,
                   (p.price * ci.quantity) AS line_total
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.product_id
            JOIN categories c ON p.category_id = c.category_id
            WHERE ci.user_id = %s
            ORDER BY ci.added_at DESC
        """, (user["user_id"],))
        cart_items = cur.fetchall()

    subtotal = sum(float(item["line_total"]) for item in cart_items)
    tax = round(subtotal * 0.18, 2)
    shipping = 0 if subtotal >= 50000 else 499
    total = subtotal + tax + shipping

    ctx["cart_items"] = cart_items
    ctx["subtotal"] = subtotal
    ctx["tax"] = tax
    ctx["shipping"] = shipping
    ctx["total"] = total
    ctx["applied_coupon"] = request.session.get("applied_coupon")

    return templates.TemplateResponse(request=request, name="cart.html", context=ctx)


@app.get("/checkout", response_class=HTMLResponse)
async def checkout_page(request: Request):
    """Checkout page with address and payment selection."""
    user = get_user(request)
    if not user:
        flash(request, "Please sign in to checkout.", "warning")
        return RedirectResponse("/login", status_code=303)

    ctx = base_context(request)

    with get_db() as conn:
        cur = get_cursor(conn)

        # Cart items
        cur.execute("""
            SELECT ci.*, p.product_name, p.price, p.slug, p.stock_quantity,
                   c.icon AS category_icon,
                   (p.price * ci.quantity) AS line_total
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.product_id
            JOIN categories c ON p.category_id = c.category_id
            WHERE ci.user_id = %s
        """, (user["user_id"],))
        cart_items = cur.fetchall()

        if not cart_items:
            flash(request, "Your bag is empty.", "warning")
            return RedirectResponse("/cart", status_code=303)

        # Addresses
        cur.execute("SELECT * FROM addresses WHERE user_id = %s ORDER BY is_default DESC", (user["user_id"],))
        addresses = cur.fetchall()

    subtotal = sum(float(item["line_total"]) for item in cart_items)
    applied_coupon = request.session.get("applied_coupon")
    discount = 0
    if applied_coupon:
        discount = float(applied_coupon.get("discount_amount", 0))
    tax = round((subtotal - discount) * 0.18, 2)
    shipping = 0 if subtotal >= 50000 else 499
    total = subtotal - discount + tax + shipping

    ctx["cart_items"] = cart_items
    ctx["addresses"] = addresses
    ctx["subtotal"] = subtotal
    ctx["discount"] = discount
    ctx["tax"] = tax
    ctx["shipping"] = shipping
    ctx["total"] = total
    ctx["applied_coupon"] = applied_coupon

    return templates.TemplateResponse(request=request, name="checkout.html", context=ctx)


@app.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request):
    """My orders page."""
    user = get_user(request)
    if not user:
        return RedirectResponse("/login", status_code=303)

    ctx = base_context(request)

    with get_db() as conn:
        cur = get_cursor(conn)
        cur.execute("""
            SELECT * FROM orders
            WHERE user_id = %s
            ORDER BY placed_at DESC
        """, (user["user_id"],))
        orders = cur.fetchall()

        for order in orders:
            cur.execute("""
                SELECT oi.*, p.slug, c.icon AS category_icon
                FROM order_items oi
                JOIN products p ON oi.product_id = p.product_id
                JOIN categories c ON p.category_id = c.category_id
                WHERE oi.order_id = %s
            """, (order["order_id"],))
            items_list = cur.fetchall()
            order["order_items"] = items_list
            order["items"] = items_list

    ctx["orders"] = orders
    return templates.TemplateResponse(request=request, name="orders.html", context=ctx)


@app.get("/order/{order_number}", response_class=HTMLResponse)
async def order_detail_page(request: Request, order_number: str):
    """Order confirmation / detail page."""
    user = get_user(request)
    if not user:
        return RedirectResponse("/login", status_code=303)

    ctx = base_context(request)

    with get_db() as conn:
        cur = get_cursor(conn)
        cur.execute("SELECT * FROM orders WHERE order_number = %s AND user_id = %s",
                    (order_number, user["user_id"]))
        order = cur.fetchone()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        cur.execute("""
            SELECT oi.*, p.slug, c.icon AS category_icon
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            JOIN categories c ON p.category_id = c.category_id
            WHERE oi.order_id = %s
        """, (order["order_id"],))
        order_items_list = cur.fetchall()
        order["order_items"] = order_items_list
        order["items"] = order_items_list

        # Shipping address
        if order.get("shipping_address_id"):
            cur.execute("SELECT * FROM addresses WHERE address_id = %s", (order["shipping_address_id"],))
            order["address"] = cur.fetchone()

    ctx["order"] = order
    return templates.TemplateResponse(request=request, name="order_confirmation.html", context=ctx)


@app.get("/wishlist", response_class=HTMLResponse)
async def wishlist_page(request: Request):
    """Wishlist page."""
    user = get_user(request)
    if not user:
        return RedirectResponse("/login", status_code=303)

    ctx = base_context(request)

    with get_db() as conn:
        cur = get_cursor(conn)
        cur.execute("""
            SELECT p.*, c.category_name, c.icon AS category_icon, w.added_at AS wishlisted_at
            FROM wishlist w
            JOIN products p ON w.product_id = p.product_id
            JOIN categories c ON p.category_id = c.category_id
            WHERE w.user_id = %s
            ORDER BY w.added_at DESC
        """, (user["user_id"],))
        ctx["wishlist_items"] = cur.fetchall()

    return templates.TemplateResponse(request=request, name="wishlist.html", context=ctx)


@app.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    """User profile page."""
    user = get_user(request)
    if not user:
        return RedirectResponse("/login", status_code=303)

    ctx = base_context(request)

    with get_db() as conn:
        cur = get_cursor(conn)

        # Fresh user data
        cur.execute("SELECT * FROM users WHERE user_id = %s", (user["user_id"],))
        ctx["profile"] = cur.fetchone()

        # Addresses
        cur.execute("SELECT * FROM addresses WHERE user_id = %s ORDER BY is_default DESC", (user["user_id"],))
        ctx["addresses"] = cur.fetchall()

        # Order count
        cur.execute("SELECT COUNT(*) AS cnt FROM orders WHERE user_id = %s", (user["user_id"],))
        ctx["order_count"] = cur.fetchone()["cnt"]

    return templates.TemplateResponse(request=request, name="profile.html", context=ctx)


# ─── Auth Pages ───────────────────────────────────────────────

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if get_user(request):
        return RedirectResponse("/", status_code=303)
    ctx = base_context(request)
    return templates.TemplateResponse(request=request, name="login.html", context=ctx)


@app.post("/login")
async def login_submit(request: Request, email: str = Form(...), password: str = Form(...)):
    with get_db() as conn:
        cur = get_cursor(conn)
        cur.execute("SELECT * FROM users WHERE email = %s AND is_active = TRUE", (email,))
        user = cur.fetchone()

    if not user or not verify_password(password, user["password_hash"]):
        flash(request, "Invalid email or password.", "error")
        return RedirectResponse("/login", status_code=303)

    # Store user in session (exclude sensitive fields)
    request.session["user"] = {
        "user_id": user["user_id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "phone": user.get("phone"),
        "role": user["role"],
    }
    flash(request, f"Welcome back, {user['full_name']}!", "success")

    # Redirect admin to dashboard
    if user["role"] == "admin":
        return RedirectResponse("/admin", status_code=303)
    return RedirectResponse("/", status_code=303)


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    if get_user(request):
        return RedirectResponse("/", status_code=303)
    ctx = base_context(request)
    return templates.TemplateResponse(request=request, name="register.html", context=ctx)


@app.post("/register")
async def register_submit(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    password: str = Form(...),
    confirm_password: str = Form(...),
):
    # Validate
    if password != confirm_password:
        flash(request, "Passwords do not match.", "error")
        return RedirectResponse("/register", status_code=303)

    if len(password) < 6:
        flash(request, "Password must be at least 6 characters.", "error")
        return RedirectResponse("/register", status_code=303)

    with get_db() as conn:
        cur = get_cursor(conn)

        # Check duplicate email
        cur.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            flash(request, "An account with this email already exists.", "error")
            return RedirectResponse("/register", status_code=303)

        # Create user
        password_hash = hash_password(password)
        cur.execute("""
            INSERT INTO users (full_name, email, phone, password_hash, role)
            VALUES (%s, %s, %s, %s, 'customer')
        """, (full_name, email, phone or None, password_hash))

        user_id = cur.lastrowid

    # Auto-login
    request.session["user"] = {
        "user_id": user_id,
        "full_name": full_name,
        "email": email,
        "phone": phone or None,
        "role": "customer",
    }
    flash(request, f"Welcome to Apple Store, {full_name}! Your account has been created.", "success")
    return RedirectResponse("/", status_code=303)


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)


# ─── Cart API ─────────────────────────────────────────────────

@app.post("/api/cart/add")
async def api_cart_add(request: Request):
    user = get_user(request)
    if not user:
        return JSONResponse({"success": False, "message": "Please sign in first."}, status_code=401)

    body = await request.json()
    product_id = body.get("product_id")
    quantity = body.get("quantity", 1)

    if not product_id or quantity < 1:
        return JSONResponse({"success": False, "message": "Invalid product or quantity."}, status_code=400)

    with get_db() as conn:
        cur = get_cursor(conn)

        # Check product exists and has stock
        cur.execute("SELECT product_id, product_name, stock_quantity, price FROM products WHERE product_id = %s AND is_active = TRUE", (product_id,))
        product = cur.fetchone()
        if not product:
            return JSONResponse({"success": False, "message": "Product not found."}, status_code=404)

        if product["stock_quantity"] < quantity:
            return JSONResponse({"success": False, "message": f"Only {product['stock_quantity']} units available."}, status_code=400)

        # Upsert cart item
        cur.execute("""
            INSERT INTO cart_items (user_id, product_id, quantity)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity)
        """, (user["user_id"], product_id, quantity))

        # Get updated cart count
        cur.execute("SELECT COALESCE(SUM(quantity), 0) AS cnt FROM cart_items WHERE user_id = %s", (user["user_id"],))
        cart_count = int(cur.fetchone()["cnt"])

    return JSONResponse({
        "success": True,
        "message": f"{product['product_name']} added to your bag!",
        "cart_count": cart_count,
    })


@app.put("/api/cart/update")
async def api_cart_update(request: Request):
    user = get_user(request)
    if not user:
        return JSONResponse({"success": False, "message": "Please sign in."}, status_code=401)

    body = await request.json()
    product_id = body.get("product_id")
    quantity = body.get("quantity", 0)

    with get_db() as conn:
        cur = get_cursor(conn)

        if quantity <= 0:
            cur.execute("DELETE FROM cart_items WHERE user_id = %s AND product_id = %s",
                        (user["user_id"], product_id))
        else:
            # Check stock
            cur.execute("SELECT stock_quantity FROM products WHERE product_id = %s", (product_id,))
            prod = cur.fetchone()
            if prod and quantity > prod["stock_quantity"]:
                return JSONResponse({"success": False, "message": f"Only {prod['stock_quantity']} in stock."}, status_code=400)

            cur.execute("UPDATE cart_items SET quantity = %s WHERE user_id = %s AND product_id = %s",
                        (quantity, user["user_id"], product_id))

        # Return updated totals
        cur.execute("""
            SELECT COALESCE(SUM(p.price * ci.quantity), 0) AS subtotal,
                   COALESCE(SUM(ci.quantity), 0) AS cart_count
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.product_id
            WHERE ci.user_id = %s
        """, (user["user_id"],))
        totals = cur.fetchone()

    subtotal = float(totals["subtotal"])
    tax = round(subtotal * 0.18, 2)
    shipping = 0 if subtotal >= 50000 else 499
    total = subtotal + tax + shipping

    return JSONResponse({
        "success": True,
        "cart_count": int(totals["cart_count"]),
        "subtotal": subtotal,
        "tax": tax,
        "shipping": shipping,
        "total": total,
    })


@app.delete("/api/cart/remove/{product_id}")
async def api_cart_remove(request: Request, product_id: int):
    user = get_user(request)
    if not user:
        return JSONResponse({"success": False, "message": "Please sign in."}, status_code=401)

    with get_db() as conn:
        cur = get_cursor(conn)
        cur.execute("DELETE FROM cart_items WHERE user_id = %s AND product_id = %s",
                    (user["user_id"], product_id))

        cur.execute("SELECT COALESCE(SUM(quantity), 0) AS cnt FROM cart_items WHERE user_id = %s", (user["user_id"],))
        cart_count = int(cur.fetchone()["cnt"])

    return JSONResponse({"success": True, "message": "Removed from bag.", "cart_count": cart_count})


# ─── Coupon API ───────────────────────────────────────────────

@app.post("/api/coupon/apply")
async def api_apply_coupon(request: Request):
    user = get_user(request)
    if not user:
        return JSONResponse({"success": False, "message": "Please sign in."}, status_code=401)

    body = await request.json()
    code = body.get("code", "").strip().upper()

    if not code:
        return JSONResponse({"success": False, "message": "Please enter a coupon code."}, status_code=400)

    with get_db() as conn:
        cur = get_cursor(conn)

        # Find coupon
        cur.execute("""
            SELECT * FROM coupons
            WHERE code = %s AND is_active = TRUE
              AND valid_from <= NOW() AND valid_until >= NOW()
              AND (usage_limit IS NULL OR times_used < usage_limit)
        """, (code,))
        coupon = cur.fetchone()

        if not coupon:
            # Remove any previously applied coupon
            request.session.pop("applied_coupon", None)
            return JSONResponse({"success": False, "message": "Invalid or expired coupon code."}, status_code=400)

        # Calculate cart subtotal
        cur.execute("""
            SELECT COALESCE(SUM(p.price * ci.quantity), 0) AS subtotal
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.product_id
            WHERE ci.user_id = %s
        """, (user["user_id"],))
        subtotal = float(cur.fetchone()["subtotal"])

        if subtotal < float(coupon["min_order_amount"]):
            return JSONResponse({
                "success": False,
                "message": f"Minimum order of ₹{int(coupon['min_order_amount']):,} required for this coupon."
            }, status_code=400)

        # Calculate discount
        if coupon["discount_type"] == "percentage":
            discount = subtotal * float(coupon["discount_value"]) / 100
            if coupon["max_discount_amount"]:
                discount = min(discount, float(coupon["max_discount_amount"]))
        else:
            discount = float(coupon["discount_value"])

        discount = round(discount, 2)

    # Store in session
    request.session["applied_coupon"] = {
        "coupon_id": coupon["coupon_id"],
        "code": coupon["code"],
        "description": coupon["description"],
        "discount_amount": discount,
        "discount_type": coupon["discount_type"],
        "discount_value": float(coupon["discount_value"]),
    }

    tax = round((subtotal - discount) * 0.18, 2)
    shipping = 0 if subtotal >= 50000 else 499
    total = subtotal - discount + tax + shipping

    return JSONResponse({
        "success": True,
        "message": f"Coupon '{code}' applied! You save ₹{int(discount):,}.",
        "discount": discount,
        "subtotal": subtotal,
        "tax": tax,
        "shipping": shipping,
        "total": total,
        "coupon_description": coupon["description"],
    })


@app.api_route("/api/coupon/remove", methods=["POST", "DELETE"])
async def api_remove_coupon(request: Request):
    request.session.pop("applied_coupon", None)
    return JSONResponse({"success": True, "message": "Coupon removed."})


# ─── Wishlist API ─────────────────────────────────────────────

@app.post("/api/wishlist/toggle/{product_id}")
async def api_wishlist_toggle(request: Request, product_id: int):
    user = get_user(request)
    if not user:
        return JSONResponse({"success": False, "message": "Please sign in."}, status_code=401)

    with get_db() as conn:
        cur = get_cursor(conn)

        cur.execute("SELECT wishlist_id FROM wishlist WHERE user_id = %s AND product_id = %s",
                    (user["user_id"], product_id))
        existing = cur.fetchone()

        if existing:
            cur.execute("DELETE FROM wishlist WHERE wishlist_id = %s", (existing["wishlist_id"],))
            action = "removed"
        else:
            cur.execute("INSERT INTO wishlist (user_id, product_id) VALUES (%s, %s)",
                        (user["user_id"], product_id))
            action = "added"

        cur.execute("SELECT COUNT(*) AS cnt FROM wishlist WHERE user_id = %s", (user["user_id"],))
        wishlist_count = int(cur.fetchone()["cnt"])

    return JSONResponse({
        "success": True,
        "action": action,
        "message": f"{'Added to' if action == 'added' else 'Removed from'} wishlist.",
        "wishlist_count": wishlist_count,
    })


# ─── Review API ───────────────────────────────────────────────

@app.post("/api/reviews")
async def api_submit_review(request: Request):
    user = get_user(request)
    if not user:
        return JSONResponse({"success": False, "message": "Please sign in to review."}, status_code=401)

    body = await request.json()
    product_id = body.get("product_id")
    rating = body.get("rating")
    title = body.get("title", "")
    review_text = body.get("review_text") or body.get("text", "")

    if not product_id or not rating or rating < 1 or rating > 5:
        return JSONResponse({"success": False, "message": "Invalid review data."}, status_code=400)

    with get_db() as conn:
        cur = get_cursor(conn)

        # Check if already reviewed
        cur.execute("SELECT review_id FROM reviews WHERE product_id = %s AND user_id = %s",
                    (product_id, user["user_id"]))
        if cur.fetchone():
            return JSONResponse({"success": False, "message": "You've already reviewed this product."}, status_code=409)

        # Check verified purchase
        cur.execute("""
            SELECT 1 FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            WHERE o.user_id = %s AND oi.product_id = %s AND o.order_status NOT IN ('Cancelled', 'Returned')
        """, (user["user_id"], product_id))
        is_verified = cur.fetchone() is not None

        cur.execute("""
            INSERT INTO reviews (product_id, user_id, rating, title, review_text, is_verified_purchase)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (product_id, user["user_id"], rating, title or None, review_text or None, is_verified))

        # Update product rating
        cur.execute("""
            UPDATE products
            SET rating_avg = (SELECT AVG(rating) FROM reviews WHERE product_id = %s),
                rating_count = (SELECT COUNT(*) FROM reviews WHERE product_id = %s)
            WHERE product_id = %s
        """, (product_id, product_id, product_id))

    return JSONResponse({
        "success": True,
        "message": "Thank you for your review!",
        "is_verified": is_verified,
    })


# ─── Place Order ──────────────────────────────────────────────

@app.post("/place-order")
async def place_order(
    request: Request,
    address_id: int = Form(None),
    address_line1: str = Form(""),
    address_line2: str = Form(""),
    city: str = Form(""),
    state: str = Form(""),
    pincode: str = Form(""),
    payment_method: str = Form("COD"),
    notes: str = Form(""),
):
    user = get_user(request)
    if not user:
        return RedirectResponse("/login", status_code=303)

    with get_db() as conn:
        cur = get_cursor(conn)

        # Get cart items
        cur.execute("""
            SELECT ci.*, p.product_name, p.price, p.stock_quantity, p.product_id
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.product_id
            WHERE ci.user_id = %s
        """, (user["user_id"],))
        cart_items = cur.fetchall()

        if not cart_items:
            flash(request, "Your bag is empty.", "warning")
            return RedirectResponse("/cart", status_code=303)

        # Validate stock
        for item in cart_items:
            if item["quantity"] > item["stock_quantity"]:
                flash(request, f"'{item['product_name']}' has only {item['stock_quantity']} in stock.", "error")
                return RedirectResponse("/cart", status_code=303)

        # Handle address
        shipping_address_id = address_id
        if not shipping_address_id and address_line1:
            cur.execute("""
                INSERT INTO addresses (user_id, label, address_line1, address_line2, city, state, pincode)
                VALUES (%s, 'Home', %s, %s, %s, %s, %s)
            """, (user["user_id"], address_line1, address_line2 or None, city, state, pincode))
            shipping_address_id = cur.lastrowid

        # Calculate totals
        subtotal = sum(float(item["price"]) * item["quantity"] for item in cart_items)

        applied_coupon = request.session.get("applied_coupon")
        discount = 0
        coupon_id = None
        if applied_coupon:
            discount = float(applied_coupon.get("discount_amount", 0))
            coupon_id = applied_coupon.get("coupon_id")

        tax = round((subtotal - discount) * 0.18, 2)
        shipping_fee = 0 if subtotal >= 50000 else 499
        total = subtotal - discount + tax + shipping_fee

        order_number = generate_order_number()

        # Insert order
        cur.execute("""
            INSERT INTO orders (user_id, order_number, subtotal, discount_amount, tax_amount,
                                shipping_fee, total_amount, coupon_id, shipping_address_id,
                                payment_method, payment_status, order_status, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Placed', %s)
        """, (
            user["user_id"], order_number, subtotal, discount, tax,
            shipping_fee, total, coupon_id, shipping_address_id,
            payment_method, "Paid" if payment_method != "COD" else "Pending",
            notes or None,
        ))
        order_id = cur.lastrowid

        # Insert order items and reduce stock
        for item in cart_items:
            line_total = float(item["price"]) * item["quantity"]
            cur.execute("""
                INSERT INTO order_items (order_id, product_id, product_name, unit_price, quantity, total_price)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (order_id, item["product_id"], item["product_name"], item["price"], item["quantity"], line_total))

            cur.execute("UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s",
                        (item["quantity"], item["product_id"]))

        # Update coupon usage
        if coupon_id:
            cur.execute("UPDATE coupons SET times_used = times_used + 1 WHERE coupon_id = %s", (coupon_id,))

        # Clear cart and coupon
        cur.execute("DELETE FROM cart_items WHERE user_id = %s", (user["user_id"],))

    request.session.pop("applied_coupon", None)
    flash(request, f"Order {order_number} placed successfully! 🎉", "success")
    return RedirectResponse(f"/order/{order_number}", status_code=303)


# ─── Address API ──────────────────────────────────────────────

@app.post("/api/address/add")
async def api_add_address(request: Request):
    user = get_user(request)
    if not user:
        return JSONResponse({"success": False, "message": "Please sign in."}, status_code=401)

    body = await request.json()

    with get_db() as conn:
        cur = get_cursor(conn)

        if body.get("is_default"):
            cur.execute("UPDATE addresses SET is_default = FALSE WHERE user_id = %s", (user["user_id"],))

        cur.execute("""
            INSERT INTO addresses (user_id, label, address_line1, address_line2, city, state, pincode, country, is_default)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user["user_id"], body.get("label", "Home"),
            body["address_line1"], body.get("address_line2"),
            body["city"], body["state"], body["pincode"],
            body.get("country", "India"), body.get("is_default", False),
        ))

    return JSONResponse({"success": True, "message": "Address saved."})


@app.delete("/api/address/{address_id}")
async def api_delete_address(request: Request, address_id: int):
    user = get_user(request)
    if not user:
        return JSONResponse({"success": False, "message": "Please sign in."}, status_code=401)

    with get_db() as conn:
        cur = get_cursor(conn)
        cur.execute("DELETE FROM addresses WHERE address_id = %s AND user_id = %s",
                    (address_id, user["user_id"]))

    return JSONResponse({"success": True, "message": "Address deleted."})


# ─── Admin Dashboard ──────────────────────────────────────────

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    user = get_user(request)
    if not user or user.get("role") != "admin":
        flash(request, "Admin access required.", "error")
        return RedirectResponse("/login", status_code=303)

    ctx = base_context(request)

    with get_db() as conn:
        cur = get_cursor(conn)

        cur.execute("SELECT COUNT(*) AS cnt FROM products WHERE is_active = TRUE")
        total_products = cur.fetchone()["cnt"]

        cur.execute("SELECT COUNT(*) AS cnt FROM orders")
        total_orders = cur.fetchone()["cnt"]

        cur.execute("SELECT COALESCE(SUM(total_amount), 0) AS rev FROM orders WHERE order_status != 'Cancelled'")
        total_revenue = float(cur.fetchone()["rev"])

        cur.execute("SELECT COUNT(*) AS cnt FROM users WHERE role = 'customer'")
        total_customers = cur.fetchone()["cnt"]

        cur.execute("""
            SELECT o.*, u.full_name
            FROM orders o
            JOIN users u ON o.user_id = u.user_id
            ORDER BY o.placed_at DESC LIMIT 20
        """)
        recent_orders = cur.fetchall()

    ctx["stats"] = {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "total_customers": total_customers,
    }
    ctx["recent_orders"] = recent_orders

    return templates.TemplateResponse(request=request, name="admin/dashboard.html", context=ctx)


# ─── Profile Update ──────────────────────────────────────────

@app.post("/profile/update")
async def update_profile(
    request: Request,
    full_name: str = Form(...),
    phone: str = Form(""),
):
    user = get_user(request)
    if not user:
        return RedirectResponse("/login", status_code=303)

    with get_db() as conn:
        cur = get_cursor(conn)
        cur.execute("UPDATE users SET full_name = %s, phone = %s WHERE user_id = %s",
                    (full_name, phone or None, user["user_id"]))

    request.session["user"]["full_name"] = full_name
    request.session["user"]["phone"] = phone or None
    flash(request, "Profile updated successfully!", "success")
    return RedirectResponse("/profile", status_code=303)


# ─── Run ──────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
