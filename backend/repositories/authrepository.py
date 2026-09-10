from backend.database.connection import get_connection


def find_user_by_email(email):
    conn = None

    try:
        conn = get_connection()

        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    u.id,
                    u.first_name,
                    u.last_name,
                    u.email,
                    u.password,
                    r.name AS role
                FROM tblUser u
                JOIN tblRole r ON u.role_id = r.id
                WHERE u.email = %s
                """,
                (email,)
            )

            return cursor.fetchone()

    finally:
        if conn:
            conn.close()


def find_user_by_id(user_id):
    conn = None

    try:
        conn = get_connection()

        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    u.id,
                    u.first_name,
                    u.last_name,
                    u.email,
                    r.name AS role
                FROM tblUser u
                JOIN tblRole r ON u.role_id = r.id
                WHERE u.id = %s
                """,
                (user_id,)
            )

            return cursor.fetchone()

    finally:
        if conn:
            conn.close()