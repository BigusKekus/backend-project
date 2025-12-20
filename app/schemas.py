from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class CurrencyCreateSchema(Schema):
    code = fields.Str(required=True, validate=validate.Length(min=1, max=8))
    name = fields.Str(required=True, validate=validate.Length(min=1, max=64))


class CurrencySchema(CurrencyCreateSchema):
    id = fields.Int(dump_only=True)


class UserCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    default_currency_id = fields.Int(required=False, allow_none=True)


class UserUpdateSchema(Schema):
    name = fields.Str(required=False, validate=validate.Length(min=1, max=120))
    default_currency_id = fields.Int(required=False, allow_none=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    default_currency = fields.Nested(CurrencySchema, dump_only=True)
    default_currency_id = fields.Int(dump_only=True)


class CategoryCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))


class CategorySchema(CategoryCreateSchema):
    id = fields.Int(dump_only=True)


class RecordCreateSchema(Schema):
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)

    # підтримка sum або amount (щоб не ламати ЛР2)
    sum = fields.Float(required=False)
    amount = fields.Float(required=False)

    currency_id = fields.Int(required=False, allow_none=True)

    @validates_schema
    def validate_amount(self, data, **kwargs):
        has_sum = "sum" in data and data["sum"] is not None
        has_amount = "amount" in data and data["amount"] is not None
        if not has_sum and not has_amount:
            raise ValidationError("Provide 'sum' or 'amount'.")
        if has_sum and has_amount:
            raise ValidationError("Provide only one: 'sum' or 'amount'.")


class RecordSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    category_id = fields.Int()
    currency_id = fields.Int()
    created_at = fields.DateTime()
    amount = fields.Float()
    currency = fields.Nested(CurrencySchema, dump_only=True)


class RecordQuerySchema(Schema):
    user_id = fields.Int(required=False)
    category_id = fields.Int(required=False)

    @validates_schema
    def validate_filters(self, data, **kwargs):
        if not data.get("user_id") and not data.get("category_id"):
            raise ValidationError("Provide at least 'user_id' or 'category_id'.")
