from flask import Blueprint, request, jsonify, current_app, g
from app.extensions import db, bcrypt
from app.models import User
from utils.decorators import jwt_required
import jwt
import datetime

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(
        username=username,
        password_hash=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

  
    if not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Incorrect password"}), 401

   
    token = jwt.encode(
        {
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256"
    )

   
    return jsonify({
        "message": "Login successful",
        "token": token
    }), 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required
def me():

        user = User.query.get(g.current_user.id)

        return jsonify({
            "id": user.id,
            "username": user.username
        }), 200

 


