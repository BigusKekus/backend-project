from flask import Flask

from app.extensions import api, db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py", silent=True)
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    from app.views import blp as core_blp
    from app.user_routes import blp as user_blp
    from app.category_routes import blp as category_blp
    from app.record_routes import blp as record_blp
    from app.currency_routes import blp as currency_blp

    api.register_blueprint(core_blp)
    api.register_blueprint(user_blp)
    api.register_blueprint(category_blp)
    api.register_blueprint(record_blp)
    api.register_blueprint(currency_blp)

    return app
