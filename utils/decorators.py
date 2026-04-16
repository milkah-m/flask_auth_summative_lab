from functools import wraps
from flask import request, jsonify, current_app, g
import jwt
from app.models import User


def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None

        auth_header = request.headers.get("Authorization")

        if auth_header:
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Token missing"}), 401

        try:
            data = jwt.decode(
                token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"]
            )

            user = User.query.get(data["user_id"])

            if not user:
                return jsonify({"error": "User not found"}), 404

            g.current_user = user   

        except Exception:
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(*args, **kwargs)

    return wrapper