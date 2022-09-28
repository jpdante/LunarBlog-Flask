from flask import Blueprint, render_template, request, current_app, redirect, Response

from ..models.account import Account
from ..models.category import Category
from ..models.post import Post
from ..models.postCategory import PostCategory
from ..models.comment import Comment
from datetime import datetime
from ..extensions import db
import jwt
import hashlib
import markdown
import html

defaultBp = Blueprint('defaultBp', __name__)

def checkUser():
    token = request.cookies.get("token")
    accountObj = None
    
    if not token:
        return accountObj
    
    try:
        accountObj = jwt.decode(
            token, current_app.config['jwt-key'], ['HS256'])
        accountObj['hashedEmail'] = hashlib.md5(
            bytearray(accountObj['email'], 'utf-8')).hexdigest()
    except jwt.InvalidSignatureError:
        return redirect('/', code=302)

    return accountObj

@defaultBp.route('/')
def home():
    check = checkUser()
    if type(check) == Response:
        return check
        
    categories = Category.query.all()
    posts = Post.query.order_by(Post.createdAt.desc()).all()
    for post in posts:
        post.htmlContent = markdown.markdown(post.content)
        post.categories = []
        for postCategory in PostCategory.query.filter_by(postId=post.id):
            for category in categories:
                if postCategory.categoryId == category.id:
                    post.categories.append(category)
    return render_template('default/home.html', page='',accountObj=check, categories=categories, posts=posts)

@defaultBp.route('/category')
def category():
    check = checkUser()
    if type(check) == Response:
        return check
        
    categoryId = None
    try:
        categoryId = request.args.get("id")
    except:
        return redirect('/', code=302)

    category = Category.query.get(categoryId)
    postCategories = PostCategory.query.filter_by(categoryId=category.id)
    categories = Category.query.all()
    posts = []
    for postCategory in postCategories:
        posts.append(Post.query.get(postCategory.postId))

    for post in posts:
        post.htmlContent = markdown.markdown(post.content)
        post.categories = []
        for postCategory in PostCategory.query.filter_by(postId=post.id):
            for category in categories:
                if postCategory.categoryId == category.id:
                    post.categories.append(category)
    return render_template('default/category.html', page='',accountObj=check, categoryId=int(categoryId), categories=categories, posts=posts)

@defaultBp.route('/post')
def post():
    check = checkUser()
    if type(check) == Response:
        return check
    
    postId = None
    try:
        postId = request.args.get("id")
    except:
        return redirect('/', code=302)
    
    post = Post.query.filter_by(id=postId).first()
    if post == None:
        return redirect('/', code=302)
    post.htmlContent = markdown.markdown(post.content)
    categories = Category.query.all()
    post.categories = []
    for postCategory in PostCategory.query.filter_by(postId=post.id):
        for category in categories:
            if postCategory.categoryId == category.id:
                post.categories.append(category)
                
    comments = Comment.query.filter_by(postId=post.id).order_by(Comment.createdAt.desc()).all()
    for comment in comments:
        user = Account.query.filter_by(id=post.userId).first()
        comment.picture = hashlib.md5(bytearray(user.email, 'utf-8')).hexdigest()
        comment.name = user.name
    
    return render_template('default/post.html', accountObj=check, post=post, categories=categories, comments=comments)

@defaultBp.route('/comment', methods=["PUT"])
def comment():
    check = checkUser()
    if type(check) == Response:
        return check
    
    if check == None:
        return Response('{ "status": "You must login to send a comment." }', status=403, mimetype='application/json')
    
    postId = None
    content = None
    try:
        postId = request.form["postId"]
    except:
        return Response('{ "status": "Post id required" }', status=400, mimetype='application/json')
    
    try:
        content = request.form["content"]
    except:
        return Response('{ "status": "Content required" }', status=400, mimetype='application/json')
    
    if not content:
        return Response('{ "status": "Invalid content" }', status=400, mimetype='application/json')
        
    post: Post = Post.query.get(postId)
    if (post == None):
        return Response('{ "status": "Post not found" }', status=404, mimetype='application/json')
    
    comment = Comment(postId=post.id,userId=check['sub'],content=html.escape(content),createdAt=datetime.now())
    db.session.add(comment)
    db.session.commit()
    
    return Response('{ "status": "Ok" }', status=200, mimetype='application/json')