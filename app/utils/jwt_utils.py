import jwt
import uuid
from functools import wraps
from flask import request, jsonify, g

from datetime import datetime, timedelta, timezone

from app.config.settings import (
    JWT_ACCESS_TOKEN_EXPIRES,
    JWT_SECRET_KEY
)
from app.utils.token_blocklist import TOKEN_BLOCKLIST

def create_access_token(identity, role):

    jti = str(uuid.uuid4())

    payload = {
        "sub": str(identity),
        "role": role,
        "jti": jti,
        "exp": (datetime.now(timezone.utc) + timedelta (seconds=JWT_ACCESS_TOKEN_EXPIRES)
        )
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
            g.jwt_payload  = payload
            g.user_id = payload.get("sub")
            g.user_role = payload.get("role")
            g.jti = jti

            print(f"Setting g.user_id = {payload.get('sub')}")
            print(f"Setting g.user_role = {payload.get('role')}")

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired. Please login again."}), 401
        
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token."}), 401
        
        return f(*args, **kwargs)
    
    return decorated


def role_required(required_role):
    def decorator(f):
        @wraps(f)

        def decorated(*args, **kwargs):
            user_role = g.user_role

            if not user_role or user_role.lower() != required_role.lower():
                return jsonify({"message": f"Access denied. {required_role} role required."}), 401
            
            return f(*args, **kwargs)
        
        return decorated
    
    return decorator