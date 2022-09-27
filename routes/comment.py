from flask import Blueprint, render_template, request, current_app
from ..extensions import db
from ..models.account import Account
from ..models.category import Category
import jwt
import hashlib

commentBp = Blueprint('commentBp', __name__)