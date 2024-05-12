import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

database = SQLAlchemy()
login = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_mapping({
        "SECRET_KEY": os.urandom(24),
        "SQLALCHEMY_TRACK_NOTIFICATIONS": False,
        "SQLALCHEMY_DATABASE_URI": 'sqlite:///subify.db'
    })

    from subify.models import User, Sub
    database.init_app(app)

    with app.app_context():
        database.create_all()

    login.init_app(app)
    login.user_loader(lambda user_id: models.User.query.get(user_id))

    from subify.auth.routes import auth
    from subify.main.routes import main
    from subify.sub.routes import sub
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(sub)

    return app
