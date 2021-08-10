from flask import  Blueprint,request
from flask import  render_template, redirect, url_for, flash, session
from ..models import db
from sqlalchemy import and_, or_
from ..models import User, Userinfo
from functools import wraps

logout = Blueprint('logout', __name__)



@logout.route('/logout')
def logout_index():
    session.pop('email', None)
    return "you have logout"