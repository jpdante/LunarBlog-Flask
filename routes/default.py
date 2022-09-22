from flask import Blueprint, render_template
from ..extensions import db
from ..models.account import Account

defaultBp = Blueprint('defaultBp', __name__)

@defaultBp.route('/')
def home():
    return render_template('default/home.html')