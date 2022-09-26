# coding: utf-8
from flask import Flask
from .extensions import db, migrate
from .routes.account import accountBp
from .routes.default import defaultBp

def create_app():
    app = Flask(__name__, static_url_path='', static_folder='public')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app)

    app.register_blueprint(defaultBp)
    app.register_blueprint(accountBp)

    return app
