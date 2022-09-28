from flask import Blueprint, render_template, request, current_app
from ..models.category import Category
from ..models.post import Post
from ..models.postCategory import PostCategory
import jwt
import hashlib
import markdown

defaultBp = Blueprint('defaultBp', __name__)

@defaultBp.route('/')
def home():
    token = request.cookies.get("token")
    loggedin = False
    accountObj = None
    if token:
        try:
            accountObj = jwt.decode(token, current_app.config['jwt-key'], ['HS256'])
            accountObj['hashedEmail'] = hashlib.md5(bytearray(accountObj['email'], 'utf-8')).hexdigest()
            loggedin = True
        except jwt.InvalidSignatureError:
            pass
        
    categories = Category.query.all()
    posts = Post.query.all()
    for post in posts:
        post.htmlContent = markdown.markdown(post.content)
        post.categories = []
        for postCategory in PostCategory.query.filter_by(postId=post.id):
            for category in categories:
                if postCategory.categoryId == category.id:
                    post.categories.append(category)
    return render_template('default/home.html', loggedin=loggedin, accountObj=accountObj, categories=categories, posts=posts)