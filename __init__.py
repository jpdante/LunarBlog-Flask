# coding: utf-8
from flask import Flask

from .models.account import Account
from .extensions import db, migrate
from .routes.account import accountBp
from .routes.default import defaultBp
from .routes.dashboard import dashboardBp
from .routes.comment import commentBp
from argon2 import PasswordHasher

def create_app():
    app = Flask(__name__, static_url_path='', static_folder='public')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['jwt-key'] = 'bananabananabananabananabananaba'

    db.init_app(app)
    migrate.init_app(app)

    app.register_blueprint(defaultBp)
    app.register_blueprint(accountBp)
    app.register_blueprint(dashboardBp)
    app.register_blueprint(commentBp)
    
    with app.app_context():
        db.create_all()
        if Account.query.filter_by(admin=True).first() == None:
            ph = PasswordHasher()
            db.session.add(Account(name='Admin', email='admin@admin.com', password=ph.hash('admin'), admin=True))
            db.session.commit()

    return app
