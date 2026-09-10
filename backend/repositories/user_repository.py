from backend.database.connection import get_connection

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
                    u.id,
                    u.first_name,
                    u.last_name,
                    u.email,
                    r.name as role,
                    r.status,
                    DATE_FORMAT(u.created_at,'%b %d, %Y %l:%i%p') AS created_at,
                    DATE_FORMAT(u.updated_at, '%b %d, %Y %l:%i%p') AS updated_at
                    FROM tblUser u
                    INNER JOIN tblRole r
                ON u.role_id = r.id
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
                    u.id,
                    u.first_name,
                    u.last_name,
                    u.email,
                    r.name as role,
                    r.status,
                    DATE_FORMAT(u.created_at, '%%b %%d, %%Y %%l:%%i%%p') AS created_at,
                    DATE_FORMAT(u.updated_at, '%%b %%d, %%Y %%l:%%i%%p') AS updated_at
                FROM tblUser u
                INNER JOIN tblRole r
                ON u.role_id = r.id
                WHERE u.id = %s;
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

def add_user_repo(first_name, last_name, email, password):
    conn = None

    try:
        conn = get_connection()

        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tblUser
                    (first_name, last_name, email, password)
                VALUES
                    (%s, %s, %s, %s)
                """,
                (first_name, last_name, email, password)
            )
            if cursor.rowcount != 1:
                conn.rollback()
                return False
            
        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        print(f"Error: {e}")
        return False
    finally:
        if conn: conn.close()
        

#======================================= 
# UPDATE USER
#=======================================

def update_user_repo(id, first_name, last_name, email, password):
    conn = None

    try:
        conn = get_connection()

        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id FROM tblUser WHERE id = %s
                """,
                (id,)
            )
            if cursor.fetchone() is None:
                conn.rollback()
                return False

            cursor.execute(
                """
                UPDATE tblUser
                SET
                    first_name = %s,
                    last_name  = %s,
                    email      = %s,
                    password   = %s
                WHERE id       = %s
                """,
                (first_name, last_name, email, password, id)
            )

        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        return False
    finally:
        if conn: conn.close()

#======================================= 
# DELETE USER
#=======================================
def delete_user_repo(id):
    conn = None

    try:
        conn = get_connection()

        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM tblUser WHERE id = %s
                """,
                (id,)
            )
            
        conn.commit()
        return True
        
    except Exception as e:
        if conn: conn.rollback()
        print(f"Error: {e}")
    finally:
        if conn: conn.close()

