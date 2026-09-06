from flask import Blueprint, request, jsonify
from jwt_utils import token_required, role_required
from config import get_connection
from werkzeug.security import generate_password_hash as generate_pwd

users = Blueprint("users", __name__)


@users.route("/api/users", methods=["GET"])
@token_required
@role_required("admin")
def get_users():
    conn = None

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    u.id,
                    CONCAT(u.last_name, ', ', u.first_name) as name,
                    u.email,
                    r.name as role,
                    r.status,
                    DATE_FORMAT(u.created_at, '%b %d, %Y %l:%i %p') as created_at,
                    DATE_FORMAT(u.updated_at, '%b %d, %Y %l:%i %p') as updated_at
                FROM tblUser u
                JOIN tblRole r
                    ON u.role_id = r.id
                """
            )
            users = cursor.fetchall()

            if users is None:
                return jsonify({"messag": "No users has found."}), 404

            return jsonify(users), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        if conn:
            conn.close()

@users.route("/api/users/<int:id>", methods=["GET"])
@token_required
@role_required("admin")
def get_user_by_id(id):
    conn = None

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
            """
                SELECT 
                    u.id,
                    CONCAT(u.last_name, ', ', u.first_name) as name,
                    u.email,
                    r.name as role,
                    r.status,
                    DATE_FORMAT(u.created_at, '%%b %%d, %%Y %%l:%%i %%p') as created_at,
                    DATE_FORMAT(u.updated_at, '%%b %%d, %%Y %%l:%%i %%p') as updated_at
                FROM tblUser u
                JOIN tblRole r
                    ON u.role_id = r.id
                WHERE u.id = %s
            """,
            (id,)
            )
            user = cursor.fetchone()

            if user is None:
                return jsonify({"message": "User has not found."}), 404

            return jsonify(user), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        if conn:
            conn.close


@users.route("/api/users", methods=["POST"])
@token_required
@role_required("admin")
def add_user():
    conn = None
    data = request.get_json()

    password = generate_pwd(data.get("password"))
    
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tblUser
                    (first_name, last_name, email, password, role_id)
                VALUES
                    (%s, %s, %s, %s, %s)
                """, 
                (
                    data.get("first_name"),
                    data.get("last_name"),
                    data.get("email"),
                    password,
                    data.get("role_id")
                )
            )
            conn.commit()

            return jsonify({"message": "User added successfully."}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"message": str(e)}), 500
    finally:
        if conn:
            conn.close()
        
