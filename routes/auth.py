from flask import Blueprint, jsonify, request, g
from config import get_connection

from jwt_utils import token_required, create_access_token, role_required
from werkzeug.security import check_password_hash as check_password

from token_blocklist import TOKEN_BLOCKLIST


auth = Blueprint('auth', __name__)


@auth.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    if data is None:
        return jsonify({"message": "Email and password is required."}), 401

    email    = data.get("email")
    password = data.get("password")
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
                    r.name as role
                FROM tblUser u
                INNER JOIN tblRole r
		        ON u.role_id = r.id
                WHERE u.email = %s;
                """,
                (email,)
            )
            user = cursor.fetchone()


            if user is None or not check_password(user["password"], password):
                return jsonify({"message": "Invalid email or password."}), 401

            access_token = create_access_token(str(user["id"]), str(user["role"]))

            return jsonify({
                "access_token": access_token,
                "user": {
                    "id": user["id"],
                    "role": user["role"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "email": user["email"]
                }
            }), 200
        
    except Exception as e:
        #return jsonify({"message": "An internal server error occured."}), 500
        return jsonify({"message": str(e)}), 500
    finally:
        if conn:
            conn.close()


@auth.route("/api/me", methods=["GET"])
@token_required
@role_required("admin")
def current_user():
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
                    r.name as role
                FROM tblUser u
                INNER JOIN tblRole r
		        ON u.role_id = r.id
                WHERE u.id = %s;
                """,
                (g.user_id,)
            )
            user = cursor.fetchone()

            return jsonify({
                "message": "Currently who logged in",
                "user": {
                    "id": user["id"],
                    "role": user["role"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "email": user["email"],
                }
            }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        if conn:
            conn.close()


@auth.route("/api/logout", methods=["POST"])
@token_required
def logout():
    jti = g.jwt_payload["jti"]
    TOKEN_BLOCKLIST.add(jti)


    return jsonify({
        "message": "Logout successfully."
    }), 200