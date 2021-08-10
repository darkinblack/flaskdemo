from flask import  Blueprint,request
from flask import  render_template, redirect, url_for, flash, session
from ..models import db
from sqlalchemy import and_, or_
from ..models import User, Userinfo
from functools import wraps

login = Blueprint('login', __name__)

def valid_login(email, password):
    user = User.query.filter(and_(User.email == email, User.password == password)).first()
    if user:
        return True
    else:
        return False


@login.route('/login', methods=['GET', 'POST'])
def login_index():
    error = None

    if request.method == 'POST':
        my_json = request.get_json()
        if valid_login(my_json['email'], my_json['password']):
            flash("success！")
            session['email'] = my_json['email']
            my_json['massage'] = "login success"
            userinfo = Userinfo.query.filter(User.email == my_json['email']).first()
            my_json['id'] = userinfo.id
            return my_json
        else:
            error = 'wrong email or password'

    return render_template('login.html', error=error)