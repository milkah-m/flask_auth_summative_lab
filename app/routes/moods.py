from flask import Blueprint, request, jsonify, g
from app.models import Mood, User
from app.extensions import db
from utils.decorators import jwt_required   # your decorator

moods_bp = Blueprint("moods", __name__, url_prefix="/moods")

@moods_bp.route("/", methods=["GET"])
@jwt_required
def get_moods():
    page = request.args.get("page", 1, type=int)
    per_page = 5

    moods_query = Mood.query.filter_by(user_id=g.current_user.id)

    paginated = moods_query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "moods": [
            {
                "id": m.id,
                "mood": m.mood,
                "note": m.note
            }
            for m in paginated.items
        ],
        "total": paginated.total,
        "page": paginated.page,
        "pages": paginated.pages
    }), 200

@moods_bp.route("/<int:id>", methods=["GET"])
@jwt_required
def get_mood(id):
    mood = Mood.query.get(id)

    if not mood:
        return jsonify({"error": "Mood not found"}), 404

    if mood.user_id != g.current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    return jsonify({
        "id": mood.id,
        "mood": mood.mood,
        "note": mood.note
    }), 200

@moods_bp.route("/", methods=["POST"])
@jwt_required
def create_mood():

    data = request.get_json()

    new_mood = Mood(
        mood=data["mood"],
        note=data.get("note"),
        user_id=g.current_user.id
    )

    db.session.add(new_mood)
    db.session.commit()

    return jsonify({
        "message": "Mood created",
        "id": new_mood.id
    }), 201

@moods_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required
def update_mood(id):
    mood = Mood.query.get(id)

    if not mood:
        return jsonify({"error": "Mood not found"}), 404

    if mood.user_id != g.current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()

    if "mood" in data:
        mood.mood = data["mood"]

    if "note" in data:
        mood.note = data["note"]

    db.session.commit()

    return jsonify({"message": "Mood updated"}), 200

@moods_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required
def delete_mood(id):
    mood = Mood.query.get(id)

    if not mood:
        return jsonify({"error": "Mood not found"}), 404

    # ownership check 🔐
    if mood.user_id != g.current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(mood)
    db.session.commit()

    return jsonify({"message": "Mood deleted"}), 200