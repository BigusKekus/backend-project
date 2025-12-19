from flask import Blueprint, jsonify, request

from app.models import DB, SEQ, Record
from app.schemas import require_float, require_int

bp = Blueprint("records", __name__)


@bp.get("/")
def list_records():
    items = [r.__dict__ for r in DB["records"].values()]
    return jsonify(items)


@bp.post("/")
def create_record():
    data = request.get_json(silent=True) or {}
    try:
        amount = require_float(data, "amount")
        category_id = require_int(data, "category_id")
        currency_id = require_int(data, "currency_id")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # проста перевірка “зв’язків”
    if category_id not in DB["categories"]:
        return jsonify({"error": "category_id not found"}), 400
    if currency_id not in DB["currencies"]:
        return jsonify({"error": "currency_id not found"}), 400

    record_id = SEQ["records"]
    SEQ["records"] += 1

    record = Record(
        id=record_id,
        amount=amount,
        category_id=category_id,
        currency_id=currency_id,
    )
    DB["records"][record_id] = record
    return jsonify(record.__dict__), 201
