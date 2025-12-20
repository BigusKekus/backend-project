from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.extensions import db
from app.models import Currency, User
from app.schemas import UserCreateSchema, UserSchema, UserUpdateSchema

blp = Blueprint("users", "users", url_prefix="", description="Users")


@blp.route("/users")
class UsersCollection(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return User.query.order_by(User.id.asc()).all()


@blp.route("/user")
class UserCreate(MethodView):
    @blp.arguments(UserCreateSchema)
    @blp.response(201, UserSchema)
    def post(self, data):
        default_currency = None

        if data.get("default_currency_id") is not None:
            default_currency = Currency.query.get(data["default_currency_id"])
            if not default_currency:
                abort(404, message="Default currency not found.")
        else:
            # зручно: якщо є UAH — ставимо її дефолтною автоматом
            default_currency = Currency.query.filter_by(code="UAH").first()

        user = User(name=data["name"].strip(), default_currency=default_currency)
        db.session.add(user)
        db.session.commit()
        return user


@blp.route("/user/<int:user_id>")
class UserItem(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message="User not found.")
        return user

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message="User not found.")
        db.session.delete(user)
        db.session.commit()
        return {"status": "deleted"}

    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserSchema)
    def patch(self, data, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message="User not found.")

        if "name" in data and data["name"] is not None:
            user.name = data["name"].strip()

        if "default_currency_id" in data:
            if data["default_currency_id"] is None:
                user.default_currency = None
            else:
                currency = Currency.query.get(data["default_currency_id"])
                if not currency:
                    abort(404, message="Currency not found.")
                user.default_currency = currency

        db.session.commit()
        return user
