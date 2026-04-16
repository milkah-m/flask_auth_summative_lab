from functools import wraps
from flask import request, jsonify, current_app, g
import jwt
from app.models import User

def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"error": "Token missing"}), 401

        try:
            data = jwt.decode(
                token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"]
            )

            g.user_id = data["user_id"]

        except:
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(*args, **kwargs)

    return wrapper
