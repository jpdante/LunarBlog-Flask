from ..extensions import db

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postId = db.Column(db.Integer(), nullable=False)
    userId = db.Column(db.Integer(), nullable=False)
    content = db.Column(db.Text, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False)