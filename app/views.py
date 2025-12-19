from flask import Flask

from app.views import bp as views_bp
from app.user_routes import bp as users_bp
from app.category_routes import bp as categories_bp
from app.currency_routes import bp as currencies_bp
from app.record_routes import bp as records_bp


def create_app() -> Flask:
    app = Flask(__name__)

    # базові ендпоінти
    app.register_blueprint(views_bp)

    # API ендпоінти (з префіксом /api)
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(currencies_bp, url_prefix="/api/currencies")
    app.register_blueprint(records_bp, url_prefix="/api/records")

    return app
