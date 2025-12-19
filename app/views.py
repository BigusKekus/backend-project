from datetime import datetime
from flask import jsonify, Flask


def register_routes(app: Flask) -> None:
    @app.route("/healthcheck", methods=["GET"])
    def healthcheck():
        return jsonify({"status": "ok", "date": datetime.utcnow().isoformat()}), 200
