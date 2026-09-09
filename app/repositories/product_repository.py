from app.database.connection import get_connection


#=======================================
#  GET ALL PRODUCTS
#=======================================
def get_products_repo(user_id):
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
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn: conn.close()

#=======================================
#  GET ID BY ID
#=======================================
def get_by_id_repo(id, user_id):
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
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn: conn.close()
        

#=======================================
#  ADD PRODUCT
#=======================================
def add_product_repo(code, name, description, qty, price, user_id):
    conn = None

    try:
        conn = get_connection()

        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tblProduct
                    (code, name, description, qty, price, user_id)
                VALUES(%s, %s, %s, %s, %s, %s)
                """,
                (code, name, description, qty, price, user_id)
            )
        conn.commit()
        return True
    
    except Exception as e:
        if conn: conn.rollback()
        print(f"Error: {e}")
    finally:
        if conn: conn.close()

#=======================================
#  UPDATE PRODUCT
#=======================================
def update_product_repo(code, name, description, qty, price, id, user_id):
    conn = None

    try:
        conn = get_connection()

        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE tblProduct
                SET 
                    code        = %s,
                    name        = %s,
                    description = %s,
                    qty         = %s,
                    price       = %s
                WHERE id        = %s
                AND user_id     = %s
                """,
                (code, name, description, qty, price, id, user_id)
            )
        conn.commit()
        return True
    
    except Exception as e:
        if conn: conn.rollback()
        print(f"Error: {e}")
    finally:
        if conn: conn.close()
        

#=======================================
#  DELETE PRODUCT
#=======================================
def delete_product_repo(id, user_id):
    conn = None

    try:
        conn = get_connection()

        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM tblProduct WHERE id = %s AND user_id = %s
                """,
                (id, user_id)
            )
        conn.commit()
        return True

    except Exception as e:
        if conn: conn.rollback()    
        print(f"Error: {e}")
    finally:
        if conn: conn.close()