from flask import Blueprint, render_template
from ..extensions import db
from ..models.account import Account

accountBp = Blueprint('accountBp', __name__)

#@accountBp.route('/account')
#def uc_list():
#    ucs_query = Account.
#    return render_template('uc_list.html', ucs=ucs_query)

@accountBp.route('/login')
def uc_list():
    return render_template('auth/login.html')