from flask import Blueprint, jsonify

blp = Blueprint("core", __name__)

@blp.get("/")
def index():
    return jsonify({"message": "backend-project"})

@blp.get("/healthcheck")
def healthcheck():
    return jsonify({"status": "ok"})
