from flask import Blueprint, render_template, request, current_app
from ..extensions import db
from ..models.account import Account
from ..models.category import Category
import jwt
import hashlib

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
    return render_template('default/home.html', loggedin=loggedin, accountObj=accountObj, categories=categories)