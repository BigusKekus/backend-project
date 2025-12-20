from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.extensions import db
from app.models import Category, Currency, Record, User
from app.schemas import RecordCreateSchema, RecordQuerySchema, RecordSchema

blp = Blueprint("records", "records", url_prefix="", description="Records")


@blp.route("/record")
class RecordCollection(MethodView):
    @blp.arguments(RecordQuerySchema, location="query")
    @blp.response(200, RecordSchema(many=True))
    def get(self, args):
        q = Record.query

        if args.get("user_id"):
            q = q.filter(Record.user_id == args["user_id"])
        if args.get("category_id"):
            q = q.filter(Record.category_id == args["category_id"])

        return q.order_by(Record.id.asc()).all()

    @blp.arguments(RecordCreateSchema)
    @blp.response(201, RecordSchema)
    def post(self, data):
        user = User.query.get(data["user_id"])
        if not user:
            abort(404, message="User not found.")

        category = Category.query.get(data["category_id"])
        if not category:
            abort(404, message="Category not found.")

        amount = data.get("amount")
        if amount is None:
            amount = data.get("sum")
        if amount is None:
            abort(400, message="Provide 'sum' or 'amount'.")

        currency = None
        if data.get("currency_id") is not None:
            currency = Currency.query.get(data["currency_id"])
            if not currency:
                abort(404, message="Currency not found.")
        else:
            currency = user.default_currency
            if not currency:
                abort(400, message="User has no default currency. Provide currency_id or set user default.")

        record = Record(
            user_id=user.id,
            category_id=category.id,
            currency_id=currency.id,
            amount=float(amount),
        )
        db.session.add(record)
        db.session.commit()
        return record


@blp.route("/record/<int:record_id>")
class RecordItem(MethodView):
    @blp.response(200, RecordSchema)
    def get(self, record_id):
        record = Record.query.get(record_id)
        if not record:
            abort(404, message="Record not found.")
        return record

    def delete(self, record_id):
        record = Record.query.get(record_id)
        if not record:
            abort(404, message="Record not found.")
        db.session.delete(record)
        db.session.commit()
        return {"status": "deleted"}
