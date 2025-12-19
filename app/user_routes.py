from flask import Blueprint, jsonify, request

from app.models import DB, SEQ, User
from app.schemas import require_str

bp = Blueprint("users", __name__)


@bp.get("/")
def list_users():
    users = [u.__dict__ for u in DB["users"].values()]
    return jsonify(users)


@bp.post("/")
def create_user():
    data = request.get_json(silent=True) or {}
    try:
        username = require_str(data, "username")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    user_id = SEQ["users"]
    SEQ["users"] += 1

    user = User(id=user_id, username=username)
    DB["users"][user_id] = user
    return jsonify(user.__dict__), 201
