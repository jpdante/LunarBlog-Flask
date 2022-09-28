from ..extensions import db

class PostCategory(db.Model):
    __tablename__ = "post_category"
    postId = db.Column(db.Integer(), primary_key=True, nullable=False)
    categoryId = db.Column(db.Integer(), primary_key=True, nullable=False)