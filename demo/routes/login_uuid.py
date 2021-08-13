from flask import  Blueprint,request
from flask import  render_template, redirect, url_for, flash, session
from ..models import db
from sqlalchemy import and_, or_
from ..models import User, Userinfo
from uuid import uuid4
from functools import wraps

login_uuid = Blueprint('login_uuid', __name__)

def valid_login(email, password):
    user = User.query.filter(and_(User.email == email, User.password == password)).first()
    if user:
        return True
    else:
        return False


@login_uuid.route('/login_uuid', methods=['GET', 'POST'])
def login_uuid_index():
    error = None

    if request.method == 'POST':
        my_json = request.get_json()
        if valid_login(my_json['email'], my_json['password']):
            session['email'] = my_json['email']
            my_json['massage'] = "login success"
            userinfo = Userinfo.query.filter(Userinfo.email == my_json['email']).first()
            my_json['id'] = userinfo.id

            #creat temp uuid
            user = User.query.filter(and_(User.email == my_json['email'], User.password == my_json['password'])).first()
            uuid_temp = uuid4().hex
            user.uuid = uuid_temp
            my_json["uuid"] = uuid_temp
            db.session.commit()
            return my_json
        else:
            error = 'wrong email or password'

    return render_template('login.html', error=error)