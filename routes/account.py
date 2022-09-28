from datetime import date
from flask import Blueprint, render_template, request, redirect, current_app, make_response
from ..extensions import db
from ..models.account import Account
from argon2 import PasswordHasher
import re
import jwt
import time

ph = PasswordHasher()

accountBp = Blueprint('accountBp', __name__)

@accountBp.route('/logout')
def logout():
    resp = make_response(redirect("/", code=302))
    resp.delete_cookie('token')
    return resp

@accountBp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        if not email:
            return render_template('auth/login.html', error='Email cannot be empty.')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render_template('auth/login.html', error='Email is not valid.')

        password = request.form["password"]
        if not password:
            return render_template('auth/login.html', error='Password cannot be empty.')

        account: Account = Account.query.filter_by(email=email).first()
        if not account:
            return render_template('auth/login.html', error='Could not find this user or password is wrong.')

        try:
            if not ph.verify(account.password, password):
                return render_template('auth/login.html', error='Could not find this user or password is wrong.')
        except:
            return render_template('auth/login.html', error='Could not find this user or password is wrong.')
      
        payload_data = {
            "sub": account.id,
            "name": account.name,
            "email": account.email,
            "iat": int(time.time()),
            "admin": account.admin
        }
        token = jwt.encode(payload=payload_data, key=current_app.config['jwt-key'], algorithm='HS256')
        resp = make_response(redirect("/", code=302))
        resp.set_cookie('token', token)
        return resp
    
    return render_template('auth/login.html')

@accountBp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        if not name:
            return render_template('auth/register.html', error='Name cannot be empty.')

        email = request.form["email"]
        if not email:
            return render_template('auth/register.html', error='Email cannot be empty.')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render_template('auth/register.html', error='Email is not valid.')

        password = request.form["password"]
        if not password:
            return render_template('auth/register.html', error='Password cannot be empty.')
        if len(password) < 8:
            return render_template('auth/register.html', error='Password must be at least 8 characters.')

        hashedPassword = ph.hash(password)
        if Account.query.filter_by(email=email).first():
            return render_template('auth/register.html', error='An account with this email already exists.')

        account: Account = Account(name=name, email=email, password=hashedPassword, admin=False)
        db.session.add(account)
        db.session.commit()
        account = Account.query.filter_by(email=email).first()

        payload_data = {
            "sub": account.id,
            "name": account.name,
            "email": account.email,
            "iat": int(time.time()),
            "admin": account.admin
        }
        token = jwt.encode(payload=payload_data, key=current_app.config['jwt-key'], algorithm='HS256')
        resp = make_response(redirect("/", code=302))
        resp.set_cookie('token', token)
        return resp
    return render_template('auth/register.html')
