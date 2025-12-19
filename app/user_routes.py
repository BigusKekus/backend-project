from __future__ import annotations

from flask import Blueprint, jsonify, request

from .models import STORE
from .schemas import ApiError, get_json, require_str

bp = Blueprint("users", __name__)

@bp.get("/users")
def list_users():
    return jsonify(list(STORE.users.values())), 200

@bp.post("/user")
def create_user():
    data = get_json(request)
    name = require_str(data, "name")
    user = STORE.create_user(name)
    return jsonify(user), 201

@bp.get("/user/<int:user_id>")
def get_user(user_id: int):
    user = STORE.users.get(user_id)
    if not user:
        raise ApiError("User not found", 404)
    return jsonify(user), 200

@bp.delete("/user/<int:user_id>")
def delete_user(user_id: int):
    ok = STORE.delete_user(user_id)
    if not ok:
        raise ApiError("User not found", 404)
    return jsonify({"status": "deleted", "user_id": user_id}), 200
