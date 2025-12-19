from __future__ import annotations
from flask import Blueprint, jsonify, request
from .models import STORE
from .schemas import ApiError, get_json, query_int, require_str

bp = Blueprint("categories", __name__)

@bp.get("/category")
def list_categories():
    return jsonify(list(STORE.categories.values())), 200

@bp.post("/category")
def create_category():
    data = get_json(request)
    name = require_str(data, "name")
    cat = STORE.create_category(name)
    return jsonify(cat), 201

@bp.delete("/category")
def delete_category():
    category_id = query_int(request.args, "category_id")
    if category_id is None:
        raise ApiError("Query param 'category_id' is required", 400)

    ok = STORE.delete_category(category_id)
    if not ok:
        raise ApiError("Category not found", 404)
    return jsonify({"status": "deleted", "category_id": category_id}), 200
