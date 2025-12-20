from datetime import datetime

from app.extensions import db


class Currency(db.Model):
    __tablename__ = "currencies"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self) -> str:
        return f"<Currency {self.code}>"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    default_currency_id = db.Column(db.Integer, db.ForeignKey("currencies.id"), nullable=True)
    default_currency = db.relationship("Currency", foreign_keys=[default_currency_id])

    records = db.relationship("Record", back_populates="user", cascade="all, delete-orphan")


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    records = db.relationship("Record", back_populates="category", cascade="all, delete-orphan")


class Record(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    currency_id = db.Column(db.Integer, db.ForeignKey("currencies.id"), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)

    user = db.relationship("User", back_populates="records")
    category = db.relationship("Category", back_populates="records")
    currency = db.relationship("Currency")
