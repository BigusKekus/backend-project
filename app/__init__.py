from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.views import blp as core_blp
    app.register_blueprint(core_blp)

    return app
