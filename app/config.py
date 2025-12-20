import os


def _db_url() -> str:
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    return "sqlite:///local.db"


SQLALCHEMY_DATABASE_URI = _db_url()
SQLALCHEMY_TRACK_MODIFICATIONS = False

API_TITLE = "Expense Tracker API"
API_VERSION = "v1"
OPENAPI_VERSION = "3.0.3"
OPENAPI_URL_PREFIX = "/"
OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
