from __future__ import annotations
from flask import Blueprint, jsonify, request
from .models import STORE
from .schemas import ApiError, get_json, query_int, require_float, require_int
bp = Blueprint("records", __name__)
@bp.post("/record")
def create_record():
    data = get_json(request)
    user_id = require_int(data, "user_id")
    category_id = require_int(data, "category_id")
    if "sum" in data:
        amount = require_float(data, "sum")
    else:
        amount = require_float(data, "amount")
    created_at = data.get("created_at") or data.get("datetime")
    if user_id not in STORE.users:
        raise ApiError("User not found", 404)
    if category_id not in STORE.categories:
        raise ApiError("Category not found", 404)
    rec = STORE.create_record(
        user_id=user_id,
        category_id=category_id,
        amount=amount,
        created_at=created_at,
    )
    return jsonify(rec), 201
@bp.get("/record/<int:record_id>")
def get_record(record_id: int):
    rec = STORE.records.get(record_id)
    if not rec:
        raise ApiError("Record not found", 404)
    return jsonify(rec), 200
@bp.delete("/record/<int:record_id>")
def delete_record(record_id: int):
    ok = STORE.delete_record(record_id)
    if not ok:
        raise ApiError("Record not found", 404)
    return jsonify({"status": "deleted", "record_id": record_id}), 200
@bp.get("/record")
def list_records():
    user_id = query_int(request.args, "user_id")
    category_id = query_int(request.args, "category_id")
    if user_id is None and category_id is None:
        raise ApiError("Provide at least one query param: user_id or category_id", 400)
    result = list(STORE.records.values())
    if user_id is not None:
        result = [r for r in result if r["user_id"] == user_id]
    if category_id is not None:
        result = [r for r in result if r["category_id"] == category_id]
    return jsonify(result), 200
