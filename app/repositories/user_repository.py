from app.database.connection import get_connection

#======================================= 
# GET ALL USERS
#=======================================
def get_users_repo():
    conn = None

    try:
        conn = get_connection()

        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    first_name,
                    last_name,
                    email,
                    DATE_FORMAT(created_at, '%b %d, %Y %l:%i%p') as created_at,
                    DATE_FORMAT(updated_at, '%b %d, %Y %l:%i%p') as updated_at
                FROM tblUser
                """
            )
            return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn: conn.close()

#======================================= 
# GET USER BY ID
#=======================================
def get_by_id_repo(id):
    conn = None

    try:
        conn = get_connection()

        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    first_name,
                    last_name,
                    email,
                    DATE_FORMAT(created_at, '%%b %%d, %%Y %%l:%%i%%p') as created_at,
                    DATE_FORMAT(updated_at, '%%b %%d, %%Y %%l:%%i%%p') as updated_at
                FROM tblUser
                WHERE id = %s
                """,
                (id,)
            )
            return cursor.fetchone()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn: conn.close()

#======================================= 
# ADD USER
#=======================================

#======================================= 
# UPDATE USER
#=======================================

#======================================= 
# DELETE USER
#=======================================

