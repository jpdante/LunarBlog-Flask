from flask import Blueprint, render_template, request, current_app, redirect, Response
from ..extensions import db
from ..models.account import Account
#from ..models.posts import Post
from ..models.category import Category
from ..models.comment import Comment
import jwt
import hashlib

dashboardBp = Blueprint('dashboardBp', __name__)


def checkUser():
    token = request.cookies.get("token")
    if not token:
        return redirect('/', code=302)

    accountObj = None
    try:
        accountObj = jwt.decode(
            token, current_app.config['jwt-key'], ['HS256'])
        accountObj['hashedEmail'] = hashlib.md5(
            bytearray(accountObj['email'], 'utf-8')).hexdigest()
    except jwt.InvalidSignatureError:
        return redirect('/', code=302)

    if not accountObj['admin']:
        return redirect('/', code=302)

    return accountObj


@dashboardBp.route('/dashboard/')
def index():
    check = checkUser()
    if type(check) == Response:
        return check

    return render_template('/dashboard/home.html', page='index', accountObj=check)


@dashboardBp.route('/dashboard/users', methods=["GET", "PUT", "PATCH", "DELETE"])
def listUsers():
    check = checkUser()
    if type(check) == Response:
        return check
    
    if request.method == "GET":
        accounts = Account.query.all()
        return render_template('/dashboard/users.html', page='users', accountObj=check, users=accounts)

    if request.method == "PATCH":
        try:
            id = request.form["id"]
        except:
            return Response('{ "status": "User id required" }', status=400, mimetype='application/json')
        
        try:
            name = request.form["name"]
        except:
            return Response('{ "status": "User name required" }', status=400, mimetype='application/json')
        
        try:
            email = request.form["email"]
        except:
            return Response('{ "status": "User email required" }', status=400, mimetype='application/json')
        
        try:
            password = request.form["password"]
        except:
            pass
        
        account = Account.query.get(id)
        if not account:
            return Response({ "status": "User not found" }, status=404, mimetype='application/json')
        if check['id'] == account.id:
            return Response({ "status": "Cannot delete yourself" }, status=403, mimetype='application/json')
        
        return Response({ "status": "ok" }, status=200, mimetype='application/json')

    if request.method == "DELETE":
        try:
            id = request.form["id"]
        except:
            return Response('{ "status": "User id required" }', status=400, mimetype='application/json')

        account = Account.query.get(id)
        if not account:
            return Response({ "status": "User not found" }, status=404, mimetype='application/json')
        if check['id'] == account.id:
            return Response({ "status": "Cannot delete yourself" }, status=403, mimetype='application/json')

        db.session.delete(account)
        db.session.commit()
        
        return Response({ "status": "ok" }, status=200, mimetype='application/json')


@dashboardBp.route('/dashboard/posts')
def listPosts():
    check = checkUser()
    if type(check) == Response:
        return check

    #posts = Post.query.all()

    # posts=posts
    return render_template('/dashboard/posts.html', page='posts', accountObj=check)


@dashboardBp.route('/dashboard/categories', methods=["GET", "PUT", "PATCH", "DELETE"])
def listCategories():
    check = checkUser()
    if type(check) == Response:
        return check
    
    if request.method == "GET":
        categories = Category.query.all()
        return render_template('/dashboard/categories.html', page='categories', accountObj=check, categories=categories)
    
    if request.method == "PUT":
        name = None
        try:
            name = request.form["name"]
        except:
            return Response('{ "status": "Category name required" }', status=400, mimetype='application/json')
        
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        category = Category.query.filter_by(name=name).first()

        return Response('{ "status": "ok", "id": "' + str(category.id) + '" }', status=200, mimetype='application/json')

    if request.method == "PATCH":
        return Response('{ "status": "ok" }', status=200, mimetype='application/json')

    if request.method == "DELETE":
        id = None
        try:
            id = request.form["id"]
        except:
            return Response('{ "status": "Category id required" }', status=400, mimetype='application/json')

        category = Category.query.get(id)
        if not category:
            return Response('{ "status": "Category not found" }', status=404, mimetype='application/json')

        db.session.delete(category)
        db.session.commit()
        
        return Response('{ "status": "ok" }', status=200, mimetype='application/json')