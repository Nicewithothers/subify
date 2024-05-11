from flask_login import UserMixin
from subify import database


class User(UserMixin, database.Model):
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(64), unique=True, nullable=False)
    name = database.Column(database.String(64), nullable=False)
    password = database.Column(database.String(64), nullable=False)
    subs = database.relationship('Sub', backref='user', lazy=True)


class Sub(UserMixin, database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(64), nullable=False)
    type = database.Column(database.String(64), nullable=False)
    occurance_type = database.Column(database.String(64), nullable=False)
    price = database.Column(database.Integer, nullable=False)
    is_paid = database.Column(database.Boolean, nullable=False, default=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)