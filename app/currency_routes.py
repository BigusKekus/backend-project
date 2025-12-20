from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.extensions import db
from app.models import Currency
from app.schemas import CurrencyCreateSchema, CurrencySchema

blp = Blueprint("currencies", "currencies", url_prefix="", description="Currencies")


@blp.route("/currency")
class CurrencyCollection(MethodView):
    @blp.response(200, CurrencySchema(many=True))
    def get(self):
        return Currency.query.order_by(Currency.id.asc()).all()

    @blp.arguments(CurrencyCreateSchema)
    @blp.response(201, CurrencySchema)
    def post(self, data):
        code = data["code"].upper().strip()

        if Currency.query.filter_by(code=code).first():
            abort(409, message="Currency with this code already exists.")

        currency = Currency(code=code, name=data["name"].strip())
        db.session.add(currency)
        db.session.commit()
        return currency


@blp.route("/currency/<int:currency_id>")
class CurrencyItem(MethodView):
    @blp.response(200, CurrencySchema)
    def get(self, currency_id: int):
        currency = Currency.query.get(currency_id)
        if not currency:
            abort(404, message="Currency not found.")
        return currency

    def delete(self, currency_id: int):
        currency = Currency.query.get(currency_id)
        if not currency:
            abort(404, message="Currency not found.")
        db.session.delete(currency)
        db.session.commit()
        return {"status": "deleted"}
