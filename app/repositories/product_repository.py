from app.database.connection import get_connection


def create(data):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tblProduct
        (code, name, description, qty, price, user_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            data["code"],
            data["name"],
            data["description"],
            data["qty"],
            data["price"],
            data["user_id"]
        )
    )

    conn.commit()

    return cursor.lastrowid