from flask import Blueprint, jsonify, request

from app.models import DB, SEQ, Currency
from app.schemas import require_str

bp = Blueprint("currencies", __name__)


@bp.get("/")
def list_currencies():
    items = [c.__dict__ for c in DB["currencies"].values()]
    return jsonify(items)


@bp.post("/")
def create_currency():
    data = request.get_json(silent=True) or {}
    try:
        code = require_str(data, "code").upper()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    currency_id = SEQ["currencies"]
    SEQ["currencies"] += 1

    currency = Currency(id=currency_id, code=code)
    DB["currencies"][currency_id] = currency
    return jsonify(currency.__dict__), 201
