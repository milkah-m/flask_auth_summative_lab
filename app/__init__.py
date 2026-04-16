from flask import Flask
from .extensions import db, bcrypt, jwt
from app.routes.auth import auth_bp
from app.routes.moods import moods_bp

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    #i used this here because this is a lab app for learning in an app for deployment i would use a .env file
    app.config["JWT_SECRET_KEY"] = "my-super-secret-key"
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(moods_bp)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app import models

    return app