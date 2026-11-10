"""
Apple Store - Seed Data Script
Drops and recreates the apple_store database, creates all tables, and inserts
comprehensive seed data including categories, products, coupons, users, and addresses.
"""
import pymysql
import json
import re
import os

# ---------------------------------------------------------------------------
# Password hashing helper — prefer bcrypt, fall back to SHA-256
# ---------------------------------------------------------------------------
try:
    import bcrypt

    def hash_password(plain: str) -> str:
        return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    print("✅ Using bcrypt for password hashing")
except ImportError:
    import hashlib

    def hash_password(plain: str) -> str:
        return hashlib.sha256(plain.encode("utf-8")).hexdigest()

    print("⚠️  bcrypt not found — falling back to SHA-256 hashing")

# ---------------------------------------------------------------------------
# DB connection helpers
# ---------------------------------------------------------------------------
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "hda77063"
DB_NAME = "apple_store"
DB_PORT = 3306

SCHEMA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")


def _connect(database=None):
    """Return a PyMySQL connection, optionally targeting a specific database."""
    params = {
        "host": DB_HOST,
        "user": DB_USER,
        "password": DB_PASS,
        "port": DB_PORT,
        "charset": "utf8mb4",
        "cursorclass": pymysql.cursors.DictCursor,
        "autocommit": True,
    }
    if database:
        params["database"] = database
    return pymysql.connect(**params)


def slugify(name: str) -> str:
    """Convert a product name to a URL-friendly slug."""
    s = name.lower()
    s = s.replace('"', '-inch').replace('"', '-inch').replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


# ===================================================================
# STEP 1 — Create / recreate the database and tables
# ===================================================================
def setup_schema():
    print("\n🔧 STEP 1: Setting up database schema …")

    # --- 1a. Drop & create database (connect WITHOUT database) ---------
    conn = _connect()
    cur = conn.cursor()
    cur.execute("DROP DATABASE IF EXISTS apple_store;")
    cur.execute("CREATE DATABASE apple_store DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print("   ✅ Database 'apple_store' created")
    cur.close()
    conn.close()

    # --- 1b. Read schema.sql and execute statements (connect WITH database)
    conn = _connect(database=DB_NAME)
    cur = conn.cursor()

    with open(SCHEMA_FILE, "r") as f:
        sql_content = f.read()

    # Remove the DROP/CREATE/USE database lines (already handled above)
    lines_to_skip = [
        "DROP DATABASE IF EXISTS apple_store;",
        "CREATE DATABASE apple_store DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
        "USE apple_store;",
    ]
    for line in lines_to_skip:
        sql_content = sql_content.replace(line, "")

    # Split on semicolons and execute each statement
    statements = [s.strip() for s in sql_content.split(";") if s.strip() and not s.strip().startswith("--")]
    for stmt in statements:
        # Skip pure comment blocks
        clean = "\n".join(l for l in stmt.split("\n") if not l.strip().startswith("--"))
        if clean.strip():
            cur.execute(clean)

    print(f"   ✅ Executed {len(statements)} schema statements — all tables created")
    cur.close()
    conn.close()


# ===================================================================
# STEP 2 — Insert seed data
# ===================================================================
def seed_data():
    print("\n🌱 STEP 2: Inserting seed data …")
    conn = _connect(database=DB_NAME)
    cur = conn.cursor()

    # ------------------------------------------------------------------
    # 2a. Categories
    # ------------------------------------------------------------------
    categories = [
        ("Mac",              "Desktops and laptops powered by Apple Silicon", "💻", 1),
        ("iPhone",           "The world's most powerful personal device",     "📱", 2),
        ("iPad",             "Your next computer is not a computer",          "📲", 3),
        ("Apple Watch",      "The ultimate device for a healthy life",        "⌚", 4),
        ("AirPods",          "Wireless audio, reimagined",                    "🎧", 5),
        ("Accessories",      "Cases, chargers, keyboards, and more",         "🔌", 6),
        ("Apple TV & Home",  "Entertainment and smart home devices",          "📺", 7),
    ]
    cur.executemany(
        "INSERT INTO categories (category_name, description, icon, display_order) VALUES (%s,%s,%s,%s)",
        categories,
    )
    print(f"   ✅ Inserted {len(categories)} categories")

    # Build a quick lookup: name → category_id
    cur.execute("SELECT category_id, category_name FROM categories")
    cat_map = {r["category_name"]: r["category_id"] for r in cur.fetchall()}

    # ------------------------------------------------------------------
    # 2b. Products (34 products)
    # ------------------------------------------------------------------
    products_raw = [
        # (category, name, description, specs_dict, price, mrp, stock, color, featured)
        # ── iPhone ──
        (
            "iPhone",
            'iPhone 16 Pro Max 256GB - Natural Titanium',
            "The most advanced iPhone ever with A18 Pro chip, 48MP camera system, and titanium design.",
            {"chip": "A18 Pro", "display": '6.9" Super Retina XDR', "camera": "48MP Fusion Camera", "battery": "Up to 33 hours video", "storage": "256GB"},
            144900, 144900, 25, "Natural Titanium", True,
        ),
        (
            "iPhone",
            'iPhone 16 Pro 128GB - Desert Titanium',
            "Pro-level performance with A18 Pro chip and pro camera system in a sleek titanium design.",
            {"chip": "A18 Pro", "display": '6.3" Super Retina XDR', "camera": "48MP Fusion Camera", "battery": "Up to 27 hours video", "storage": "128GB"},
            119900, 119900, 30, "Desert Titanium", False,
        ),
        (
            "iPhone",
            "iPhone 16 128GB - Ultramarine",
            "A new era of iPhone with the powerful A18 chip and Camera Control.",
            {"chip": "A18", "display": '6.1" Super Retina XDR', "camera": "48MP Fusion Camera", "battery": "Up to 22 hours video", "storage": "128GB"},
            79900, 79900, 40, "Ultramarine", False,
        ),
        (
            "iPhone",
            "iPhone 16 Plus 128GB - Teal",
            "Big screen. Big battery. All the power of iPhone 16 in a larger size.",
            {"chip": "A18", "display": '6.7" Super Retina XDR', "camera": "48MP Fusion Camera", "battery": "Up to 27 hours video", "storage": "128GB"},
            89900, 89900, 20, "Teal", False,
        ),
        (
            "iPhone",
            "iPhone SE (4th gen) 128GB",
            "Powerful. Colourful. Wonderful. The most affordable iPhone with Apple Intelligence.",
            {"chip": "A16 Bionic", "display": '6.1" OLED', "camera": "48MP Main Camera", "battery": "Up to 18 hours video", "storage": "128GB"},
            49900, 49900, 35, "Midnight", False,
        ),
        # ── Mac ──
        (
            "Mac",
            'MacBook Air 13" M4 (8GB/256GB)',
            "Strikingly thin and fast. M4 chip, up to 18 hours of battery life.",
            {"chip": "Apple M4", "memory": "8GB Unified", "storage": "256GB SSD", "display": '13.6" Liquid Retina', "battery": "Up to 18 hours"},
            99900, 99900, 15, "Midnight", True,
        ),
        (
            "Mac",
            'MacBook Air 15" M4 (16GB/512GB)',
            "Impossibly thin with a brilliant 15-inch Liquid Retina display and M4 chip.",
            {"chip": "Apple M4", "memory": "16GB Unified", "storage": "512GB SSD", "display": '15.3" Liquid Retina', "battery": "Up to 18 hours"},
            139900, 139900, 12, "Starlight", False,
        ),
        (
            "Mac",
            'MacBook Pro 14" M4 Pro (24GB/512GB)',
            "The most advanced pro laptop. M4 Pro chip for unmatched performance.",
            {"chip": "Apple M4 Pro", "memory": "24GB Unified", "storage": "512GB SSD", "display": '14.2" Liquid Retina XDR', "battery": "Up to 24 hours"},
            199900, 199900, 8, "Space Black", True,
        ),
        (
            "Mac",
            'MacBook Pro 16" M4 Max (48GB/1TB)',
            "Maximum performance in a pro laptop. M4 Max chip for the most demanding workflows.",
            {"chip": "Apple M4 Max", "memory": "48GB Unified", "storage": "1TB SSD", "display": '16.2" Liquid Retina XDR', "battery": "Up to 24 hours"},
            349900, 349900, 5, "Space Black", False,
        ),
        (
            "Mac",
            'iMac 24" M4 (16GB/512GB)',
            "All-in-one desktop with a gorgeous 24-inch 4.5K Retina display and M4 chip.",
            {"chip": "Apple M4", "memory": "16GB Unified", "storage": "512GB SSD", "display": '24" 4.5K Retina', "ports": "Thunderbolt / USB 4"},
            159900, 159900, 10, "Blue", False,
        ),
        (
            "Mac",
            "Mac Mini M4 (16GB/256GB)",
            "Small in size, huge in performance. The all-new Mac mini with M4 chip.",
            {"chip": "Apple M4", "memory": "16GB Unified", "storage": "256GB SSD", "ports": "Thunderbolt 4, USB-C, HDMI, Ethernet"},
            59900, 59900, 20, "Silver", False,
        ),
        (
            "Mac",
            "Mac Studio M4 Ultra",
            "Studio-grade performance with M4 Ultra chip for professionals.",
            {"chip": "Apple M4 Ultra", "memory": "192GB Unified", "storage": "2TB SSD", "ports": "Thunderbolt 5, USB-C, SDXC, HDMI"},
            399900, 399900, 3, "Silver", False,
        ),
        # ── iPad ──
        (
            "iPad",
            'iPad Pro 13" M4 (256GB WiFi)',
            "The ultimate iPad experience with the breathtakingly thin design and M4 chip.",
            {"chip": "Apple M4", "display": '13" Ultra Retina XDR', "storage": "256GB", "connector": "USB-C / Thunderbolt", "pencil": "Apple Pencil Pro"},
            112900, 112900, 14, "Space Black", True,
        ),
        (
            "iPad",
            'iPad Air 13" M3 (128GB)',
            "Powerful and versatile with M3 chip in a stunning 13-inch Liquid Retina display.",
            {"chip": "Apple M3", "display": '13" Liquid Retina', "storage": "128GB", "connector": "USB-C", "pencil": "Apple Pencil Pro"},
            79900, 79900, 18, "Purple", False,
        ),
        (
            "iPad",
            "iPad 10th Gen (64GB)",
            "Colourful. Powerful. Delightful. The essential iPad experience.",
            {"chip": "A14 Bionic", "display": '10.9" Liquid Retina', "storage": "64GB", "connector": "USB-C", "pencil": "Apple Pencil (1st gen, USB-C)"},
            34900, 34900, 30, "Blue", False,
        ),
        (
            "iPad",
            "iPad Mini 7th Gen (128GB)",
            "Small but mighty. The portable powerhouse with A17 Pro chip.",
            {"chip": "A17 Pro", "display": '8.3" Liquid Retina', "storage": "128GB", "connector": "USB-C", "pencil": "Apple Pencil Pro"},
            49900, 49900, 25, "Starlight", False,
        ),
        # ── Apple Watch ──
        (
            "Apple Watch",
            "Apple Watch Ultra 2",
            "The most rugged and capable Apple Watch. Built for adventure.",
            {"chip": "S9 SiP", "display": "49mm Always-On Retina", "case": "Titanium", "water_resistance": "100m", "battery": "Up to 36 hours"},
            89900, 89900, 10, "Natural Titanium", True,
        ),
        (
            "Apple Watch",
            "Apple Watch Series 10 (46mm GPS)",
            "Thinnest ever. Most advanced health features. Beautiful new design.",
            {"chip": "S10 SiP", "display": "46mm Always-On OLED", "case": "Aluminium", "water_resistance": "50m", "battery": "Up to 18 hours"},
            46900, 46900, 22, "Jet Black", False,
        ),
        (
            "Apple Watch",
            "Apple Watch SE (2nd Gen, 44mm)",
            "All the essentials. Light on price. The perfect way to start.",
            {"chip": "S8 SiP", "display": "44mm Retina OLED", "case": "Aluminium", "water_resistance": "50m", "battery": "Up to 18 hours"},
            29900, 29900, 28, "Midnight", False,
        ),
        # ── AirPods ──
        (
            "AirPods",
            "AirPods Pro 2 (USB-C)",
            "Intelligent noise cancellation. Immersive spatial audio. Now with USB-C.",
            {"chip": "H2", "anc": "Active Noise Cancellation", "spatial_audio": "Personalised", "battery": "Up to 6 hours (30 hours with case)", "connector": "USB-C"},
            24900, 24900, 50, "White", True,
        ),
        (
            "AirPods",
            "AirPods 4 (Active Noise Cancellation)",
            "Rebuilt from the sound up. Open-ear design with Active Noise Cancellation.",
            {"chip": "H2", "anc": "Active Noise Cancellation", "spatial_audio": "Personalised", "battery": "Up to 5 hours (30 hours with case)", "connector": "USB-C"},
            17900, 17900, 40, "White", False,
        ),
        (
            "AirPods",
            "AirPods Max (USB-C) - Midnight",
            "High-fidelity audio with industry-leading Active Noise Cancellation.",
            {"chip": "H1", "anc": "Active Noise Cancellation", "spatial_audio": "Personalised", "battery": "Up to 20 hours", "connector": "USB-C", "driver": "40mm Apple-designed"},
            59900, 59900, 8, "Midnight", False,
        ),
        # ── Accessories ──
        (
            "Accessories",
            "Apple Pencil Pro",
            "The most advanced Apple Pencil with squeeze, barrel roll, and haptic feedback.",
            {"compatibility": "iPad Pro M4, iPad Air M3", "features": "Squeeze, Barrel Roll, Haptic Feedback", "charging": "Magnetic wireless"},
            13900, 13900, 35, None, False,
        ),
        (
            "Accessories",
            "Magic Keyboard for Mac",
            "Wireless keyboard with a remarkably comfortable and precise typing experience.",
            {"connectivity": "Bluetooth / USB-C", "battery": "Rechargeable, up to 1 month", "touch_id": "Yes", "layout": "Full-size with numeric keypad"},
            10900, 10900, 20, "Silver", False,
        ),
        (
            "Accessories",
            "Magic Mouse",
            "Wireless and rechargeable with an optimised foot design for smooth tracking.",
            {"connectivity": "Bluetooth / USB-C", "battery": "Rechargeable, up to 1 month", "surface": "Multi-Touch"},
            9900, 9900, 25, "White", False,
        ),
        (
            "Accessories",
            "Magic Trackpad",
            "A large edge-to-edge glass surface with Force Touch and haptic feedback.",
            {"connectivity": "Bluetooth / USB-C", "battery": "Rechargeable, up to 1 month", "surface": "Force Touch, Multi-Touch"},
            14900, 14900, 18, "White", False,
        ),
        (
            "Accessories",
            "MagSafe Charger",
            "Effortless wireless charging perfectly aligned every time with MagSafe.",
            {"compatibility": "iPhone 12 and later", "wattage": "15W", "connector": "USB-C", "cable_length": "1m"},
            4500, 4900, 60, None, False,
        ),
        (
            "Accessories",
            "20W USB-C Power Adapter",
            "Fast, efficient USB-C power adapter for iPhone and other devices.",
            {"wattage": "20W", "connector": "USB-C", "compatibility": "iPhone, iPad, AirPods"},
            1900, 1900, 100, "White", False,
        ),
        (
            "Accessories",
            "AirTag (4 Pack)",
            "Keep track of your everyday items. Precision Finding with Ultra Wideband.",
            {"connectivity": "Bluetooth, Ultra Wideband (U1)", "battery": "CR2032 (user-replaceable)", "water_resistance": "IP67", "speaker": "Built-in"},
            12900, 12900, 45, "Silver", False,
        ),
        (
            "Accessories",
            "Apple Leather Wallet with MagSafe",
            "A slim wallet that magnetically snaps to iPhone with Find My support.",
            {"compatibility": "iPhone 12 and later with MagSafe", "material": "European leather", "cards": "Up to 3 cards", "find_my": "Yes"},
            5900, 6900, 30, "Ink", False,
        ),
        # ── Apple TV & Home ──
        (
            "Apple TV & Home",
            "Apple TV 4K (128GB WiFi+Ethernet)",
            "Cinematic in every sense. Stream, game, and work out — all in 4K Dolby Vision.",
            {"chip": "A15 Bionic", "storage": "128GB", "resolution": "4K HDR, Dolby Vision", "connectivity": "WiFi 6, Ethernet, Bluetooth 5.0", "remote": "Siri Remote"},
            17900, 17900, 15, "Black", False,
        ),
        (
            "Apple TV & Home",
            "HomePod (2nd Gen)",
            "Powerful room-filling audio with spatial audio and smart home hub capabilities.",
            {"woofer": "High-excursion", "tweeters": "5 beam-forming", "chip": "S7", "smart_home": "Matter, Thread", "siri": "Yes"},
            32900, 32900, 10, "Midnight", False,
        ),
        (
            "Apple TV & Home",
            "HomePod Mini",
            "Impressive sound. Intelligent assistant. Smart home control. All in a compact design.",
            {"driver": "Full-range driver and dual passive radiators", "chip": "S5", "smart_home": "Matter, Thread", "siri": "Yes"},
            10900, 10900, 20, "Blue", False,
        ),
    ]

    insert_product_sql = """
        INSERT INTO products
            (category_id, product_name, slug, description, specs, price, mrp,
             stock_quantity, image_url, color, is_featured, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
    """

    product_rows = []
    for cat_name, name, desc, specs, price, mrp, stock, color, featured in products_raw:
        product_rows.append((
            cat_map[cat_name],
            name,
            slugify(name),
            desc,
            json.dumps(specs),
            price,
            mrp,
            stock,
            None,          # image_url – placeholder
            color,
            featured,
        ))

    cur.executemany(insert_product_sql, product_rows)
    print(f"   ✅ Inserted {len(product_rows)} products")

    # ------------------------------------------------------------------
    # 2c. Coupons
    # ------------------------------------------------------------------
    coupons = [
        ("APPLE10",    "10% off on orders above ₹20,000",           "percentage", 10.00,   20000, 5000,  500, "2026-01-01 00:00:00", "2027-12-31 23:59:59"),
        ("FLAT2000",   "Flat ₹2,000 off on orders above ₹50,000",   "flat",       2000.00, 50000, None,  300, "2026-01-01 00:00:00", "2027-12-31 23:59:59"),
        ("WELCOME15",  "15% off for new users — min order ₹10,000",  "percentage", 15.00,   10000, 8000,  None, "2026-01-01 00:00:00", "2027-12-31 23:59:59"),
        ("STUDENT20",  "20% student discount — min order ₹30,000",   "percentage", 20.00,   30000, 15000, None, "2026-01-01 00:00:00", "2027-12-31 23:59:59"),
        ("FESTIVE5000","Flat ₹5,000 off on orders above ₹1,00,000", "flat",       5000.00, 100000, None, 200, "2026-01-01 00:00:00", "2027-12-31 23:59:59"),
    ]

    cur.executemany(
        """INSERT INTO coupons
            (code, description, discount_type, discount_value,
             min_order_amount, max_discount_amount, usage_limit,
             valid_from, valid_until)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        coupons,
    )
    print(f"   ✅ Inserted {len(coupons)} coupons")

    # ------------------------------------------------------------------
    # 2d. Users
    # ------------------------------------------------------------------
    users = [
        ("Apple Store Admin", "admin@applestore.in", hash_password("admin123"),   "9876543210", "admin"),
        ("Manoj Sahu",        "manoj@gmail.com",     hash_password("manoj123"),   "9123456780", "customer"),
        ("Rajdeep Singh",     "rajdeep@gmail.com",   hash_password("rajdeep123"), "9012345678", "customer"),
    ]

    cur.executemany(
        "INSERT INTO users (full_name, email, password_hash, phone, role) VALUES (%s,%s,%s,%s,%s)",
        users,
    )
    print(f"   ✅ Inserted {len(users)} users")

    # ------------------------------------------------------------------
    # 2e. Addresses (for Manoj Sahu — user_id = 2)
    # ------------------------------------------------------------------
    cur.execute("SELECT user_id FROM users WHERE email = 'manoj@gmail.com'")
    manoj_id = cur.fetchone()["user_id"]

    cur.execute(
        """INSERT INTO addresses
            (user_id, label, address_line1, address_line2, city, state, pincode, country, is_default)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (manoj_id, "Home", "123, Arera Colony", "Near DB Mall", "Bhopal", "Madhya Pradesh", "462016", "India", True),
    )
    print("   ✅ Inserted address for Manoj Sahu (Bhopal)")

    # ------------------------------------------------------------------
    # Commit everything
    # ------------------------------------------------------------------
    conn.commit()
    cur.close()
    conn.close()
    print("\n🎉 Seed data inserted successfully!")


# ===================================================================
# Main
# ===================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("   🍎  Apple Store — Database Setup & Seed Script")
    print("=" * 60)
    setup_schema()
    seed_data()
    print("\n" + "=" * 60)
    print("   ✅  All done! Database 'apple_store' is ready.")
    print("=" * 60)
