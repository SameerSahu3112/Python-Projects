
from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()


# GET: Fetch all products
@router.get("/")
def get_all_products():
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

    return products


# GET: Fetch a single product
@router.get("/{item_id}")
def get_product(item_id: int):

    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM products WHERE id = %s",
            (item_id,)
        )

        item = cursor.fetchone()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return item


# POST: Create a product
@router.post("/")
def create_product(item: dict):

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO products (name, price) VALUES (%s, %s)",
            (item["name"], item["price"])
        )

        conn.commit()

        product_id = cursor.lastrowid

    return {
        "message": "Product created successfully",
        "product_id": product_id
    }


# PUT: Update a product
@router.put("/{item_id}")
def update_product(item_id: int, item: dict):

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE products SET name = %s, price = %s WHERE id = %s",
            (item["name"], item["price"], item_id)
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        conn.commit()

    return {"message": "Product updated successfully"}


# DELETE: Delete a product
@router.delete("/{item_id}")
def delete_product(item_id: int):

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM products WHERE id = %s",
            (item_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        conn.commit()

    return {"message": "Product deleted successfully"}
