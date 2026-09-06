from flask import Blueprint, request, jsonify, g
from jwt_utils import token_required, role_required
from config import get_connection

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
        