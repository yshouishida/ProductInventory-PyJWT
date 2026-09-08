from app.database.connection import get_connection
from flask import g

def fetch_all_products(user_id):
    conn = None

    try:
        conn = get_connection()

        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    code,
                    name,
                    description,
                    qty,
                    price
                FROM tblProduct
                WHERE user_id = %s
                """,
                (user_id,)
            )

        return cursor.fetchall()
    
    finally:
        if conn:
            conn.close()

def fetch_by_id(id, user_id):
    conn = None

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    code,
                    name,
                    description,
                    qty,
                    price
                FROM tblProduct
                WHERE id = %s AND user_id = %s
                """,
                (id, user_id)
            )
            return cursor.fetchone()
    finally:
        if conn:
            conn.close()


def add_product(code, name, description, qty, price, user_id):
    conn = None

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tblProduct
                    (code, name, description, qty, price, user_id)
                VALUES
                    (%s, %s, %s, %s, %s, %s)
                """,
                (
                    code, name, description, qty, price, user_id
                )
            )
            return cursor.commit()
    finally:
        if conn:
            conn.close()

def update_product(id, code, name, description, qty, price, user_id):
    conn = None

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE tblProduct
                SET 
                    code = %s, 
                    name = %s, 
                    description = %s, 
                    qty = %s, 
                    price = %s
                WHERE id = %s AND user_id = %s
                """,
                (
                    id, code, name, description, qty, price, user_id
                )
            )
            return conn.commit()
        
    finally:
        if conn:
            conn.close()

def delete_product(id, user_id):
    conn = None

    try:
        conn = get_connection()

        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM tblProduct WHERE id = %s
                """,
                (id, user_id)
            )
            return conn.commit()

    finally:
        if conn:
            conn.close()
