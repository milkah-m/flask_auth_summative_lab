from .extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Mood(db.Model):
    __tablename__ = "moods"

    id = db.Column(db.Integer, primary_key=True)

    mood = db.Column(db.String(50), nullable=False)
    note = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)