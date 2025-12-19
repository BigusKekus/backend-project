from datetime import datetime

from flask import Blueprint, jsonify

bp = Blueprint("views", __name__)


@bp.get("/")
def hello():
    return jsonify({"message": "Hello from backend!"}), 200


@bp.get("/healthcheck")
def healthcheck():
    return jsonify({"status": "ok", "date": datetime.utcnow().isoformat()}), 200


def register_routes(app):
    app.register_blueprint(bp)
