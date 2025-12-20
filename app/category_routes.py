from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.extensions import db
from app.models import Category
from app.schemas import CategoryCreateSchema, CategorySchema

blp = Blueprint("categories", "categories", url_prefix="", description="Categories")


@blp.route("/category")
class CategoryCollection(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        return Category.query.order_by(Category.id.asc()).all()

    @blp.arguments(CategoryCreateSchema)
    @blp.response(201, CategorySchema)
    def post(self, data):
        name = data["name"].strip()

        if Category.query.filter_by(name=name).first():
            abort(409, message="Category already exists.")

        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return category

    def delete(self):
        from flask import request

        category_id = request.args.get("category_id", type=int)
        if not category_id:
            abort(400, message="category_id is required as query param.")

        category = Category.query.get(category_id)
        if not category:
            abort(404, message="Category not found.")

        db.session.delete(category)
        db.session.commit()
        return {"status": "deleted"}
