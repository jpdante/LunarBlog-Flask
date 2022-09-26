from flask import Blueprint, render_template
from flask import Blueprint, render_template
from ..extensions import db
from ..models.account import Account
from ..models.category import Category

defaultBp = Blueprint('defaultBp', __name__)

@defaultBp.route('/')
def home():
    categories = Category.query.all()
    return render_template('default/home.html', categories=categories)