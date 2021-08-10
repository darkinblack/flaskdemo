from flask import  Blueprint,request
from flask import  render_template, redirect, url_for, flash, session
from ..models import db
from sqlalchemy import and_, or_
from ..models import User, Userinfo
from functools import wraps

updateinfo = Blueprint('updateinfo', __name__)

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # if g.user:
        if session.get('email'):
            return func(*args, **kwargs)
        else:
            return "you havent login" #

    return wrapper

@updateinfo.route('/updateinfo', methods=['GET', 'POST'])
@login_required
def updateinfo_index():

    email = session.get('email')
    user = User.query.filter(User.email == email).first()
    userinfo = Userinfo.query.filter(Userinfo.email == email).first()
    my_json = request.get_json()
    if request.method == 'POST':
        try:
            userinfo.interests = my_json['interests']
        except:
            pass
        try:
            userinfo.firstname = my_json['firstname']
        except:
            pass
        try:
            userinfo.lastname = my_json['lastname']
        except:
            pass
        try:
            userinfo.age = my_json['age']
        except:
            pass
        db.session.commit()
        return "updated " + str(my_json)
    elif request.method == 'GET':
        try:
            return {'interest': userinfo.interests, 'firstname': userinfo.firstname, 'lastname': userinfo.lastname \
                , 'age': userinfo.age,'uuid':user.uuid}
        except:
            return "error"