
from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()


# GET: Fetch all users
@router.get("/")
def get_all_users():

    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, name, email FROM users")
        users = cursor.fetchall()

    return users


# GET: Fetch a single user
@router.get("/{id}")
def get_user(id: int):

    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, name, email FROM users WHERE id = %s",
            (id,)
        )

        user = cursor.fetchone()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# POST: Create a user
@router.post("/")
def create_user(user: dict):

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (user["name"], user["email"])
        )

        conn.commit()

        user_id = cursor.lastrowid

    return {
        "message": "User created successfully",
        "user_id": user_id
    }


# PUT: Update a user
@router.put("/{id}")
def update_user(id: int, user: dict):

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE users SET name = %s, email = %s WHERE id = %s",
            (user["name"], user["email"], id)
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        conn.commit()

    return {"message": "User updated successfully"}


# DELETE: Delete a user
@router.delete("/{id}")
def delete_user(id: int):

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM users WHERE id = %s",
            (id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        conn.commit()

    return {"message": "User deleted successfully"}
