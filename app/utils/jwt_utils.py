import jwt
import uuid
from functools import wraps
from flask import request, g
from app.utils.api_response import error
from datetime import datetime, timezone, timedelta
from app.utils.blocklist_token import TOKEN_BLOCKLIST
from app.config.settings import JWT_ACCESS_TOKEN_EXPIRES, JWT_SECRET_KEY


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
            return error("Authorization is required.", 401)
        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            jti = payload.get("jti")
            if jti in TOKEN_BLOCKLIST:
                return error("Token has been revoked.", 401)
            g.jti = jti
            g.user_id = int(payload.get("sub"))
            g.user_role = payload.get("role")
            g.jwt_paload = payload

        except jwt.ExpiredSignatureError:
            return error("Token has been expired. Please login again.", 401)
        except jwt.InvalidTokenError:
            return error("Invalid token.", 401)

        return f(*args, **kwargs)
    return decorated


def role_required(required_role):
    def decorator(f):
        @wraps(f)

        def decorated(*args, **kwargs):
            user_role = g.user_role

            if user_role.lower() != required_role.lower():
                return error(f"Access denied. {required_role} role required.", 401)

            return f(*args, **kwargs)
        return decorated
    return decorator            

