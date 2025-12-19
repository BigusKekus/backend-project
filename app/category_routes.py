from flask import Blueprint, jsonify, request

from app.models import DB, SEQ, Category
from app.schemas import require_str

bp = Blueprint("categories", __name__)


@bp.get("/")
def list_categories():
    items = [c.__dict__ for c in DB["categories"].values()]
    return jsonify(items)


@bp.post("/")
def create_category():
    data = request.get_json(silent=True) or {}
    try:
        name = require_str(data, "name")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    category_id = SEQ["categories"]
    SEQ["categories"] += 1

    category = Category(id=category_id, name=name)
    DB["categories"][category_id] = category
    return jsonify(category.__dict__), 201
