from __future__ import annotations
from datetime import datetime, timezone
from flask import Blueprint, Flask, jsonify
bp = Blueprint("core", __name__)
@bp.get("/")
def hello():
    return jsonify({"message": "Hello from backend-project"}), 200
@bp.get("/healthcheck")
def healthcheck():
    return (
        jsonify({"status": "ok", "date": datetime.now(timezone.utc).isoformat()}),
        200,
    )
def register_routes(app: Flask) -> None:
    app.register_blueprint(bp)
    from .user_routes import bp as user_bp
    from .category_routes import bp as category_bp
    from .record_routes import bp as record_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(record_bp)

    from .schemas import ApiError
    @app.errorhandler(ApiError)
    def handle_api_error(err: ApiError):
        return jsonify({"error": err.message}), err.status_code
