from ..extensions import db

class Account(db.Model):
    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(1024), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)