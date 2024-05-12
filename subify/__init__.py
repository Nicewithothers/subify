"""Imports"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

database = SQLAlchemy()
login = LoginManager()


def create_app():
    """App creation"""
    app = Flask(__name__)
    app.config.from_mapping({
        "SECRET_KEY": os.urandom(24),
        "SQLALCHEMY_TRACK_NOTIFICATIONS": False,
        "SQLALCHEMY_DATABASE_URI": 'sqlite:///subify.db'
    })

    from subify.models import User
    database.init_app(app)

    with app.app_context():
        database.create_all()

    login.init_app(app)

    def load_user(user_id):
        """Load user"""
        return User.query.get(user_id)

    login.user_loader(load_user)

    from subify.auth.routes import auth
    from subify.main.routes import main
    from subify.sub.routes import sub
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(sub)

    return app
