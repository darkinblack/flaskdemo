from flask import  Blueprint,request
from flask import  render_template, redirect, url_for, flash, session
from ..models import db
from sqlalchemy import and_, or_
from ..models import User, Userinfo
from functools import wraps

home = Blueprint('home', __name__)



@home.route('/home')
def home_index():

    return "it works"