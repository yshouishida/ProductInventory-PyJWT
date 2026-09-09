import jwt
import uuid
from functools import wraps
from datetime import datetime, timezone, timedelta
from app.config.settings import JWT_ACCESS_TOKEN_EXPIRES, JWT_SECRET_KEY
from flask import request, g, jsonify

from app.utils.blocklit_token import TOKEN_BLOCKLIST




def create_access_token(identity, user_role):
    jti = str(uuid.uuid4())
    payload = {
        "sub": str(identity),
        "jti": jti,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRES),
        "role": user_role
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Authorization is required."}), 401  
        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            jti = payload.get("jti")
            if jti in TOKEN_BLOCKLIST:
                return jsonify({"message": "Token has been revoked."}), 401
            g.jti = jti
            g.jwt_payload = payload
            g.user_id = int(payload.get("sub"))
            g.user_role = str(payload.get("role"))

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has been expired. Please login again."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token."}), 401
        
        return f(*args, **kwargs)
    
    return decorated


def role_required(required_role):   
    def decorator(f):
        @wraps(f)

        def decorated(*args, **kwargs):
            user_role = g.user_role

            if user_role.lower() != required_role.lower():
                print(f"Role Required: {role_required}, User Role: {user_role}")
                return jsonify({"message": f"Access denied. {required_role} role required."}), 401

            return f(*args, **kwargs)
        return decorated
    return decorator