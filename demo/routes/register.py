from flask import  Blueprint,request
from flask import  render_template, redirect, url_for, flash, session
from ..models import db
from sqlalchemy import and_, or_
from ..models import User, Userinfo
from functools import wraps
from uuid import uuid4
from demo import add_to_firebase
register = Blueprint('register', __name__)



def valid_regist(email):
    user = User.query.filter(or_(User.email == email)).first()
    if user:
        return False
    else:
        return True


# login not working in register
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # if g.user:
        if session.get('email'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login', next=request.url))  #

    return wrapper


# check password legal
def check_number_exit(password):
    number = False
    for x in password:
        if x.isnumeric():
            number = True
            break
    return number


def check_letter_exit(password):
    for x in password:
        if x.isalpha():
            return True
    return False


def check_special_exit(password):
    for x in password:
        if x in "/?!.,_+-*/":
            return True
    return False


def check_password(password):
    if check_letter_exit(password) and check_special_exit(password) and check_number_exit(password) and len(
            password) >= 6:
        return True
    print(check_letter_exit(password), check_special_exit(password), check_number_exit(password), len(password) >= 6)
    return False



@register.route('/register', methods=['GET', 'POST'])
def register_index():
    error = None
    if request.method == 'POST':

        my_json = request.get_json()
        # check password legal
        if my_json['password1'] != my_json['password2']:
            error = "diff password"
        elif not check_password(my_json["password1"]):
            error = "too simple"
        elif not valid_regist(my_json['email']):
            error = "email has been exist"
        else:
            user = User(password=my_json['password1'], email=my_json['email'])

            # create user database
            db.session.add(user)
            db.session.commit()
            # create userinfo database with same id
            user = User.query.filter(User.email == my_json['email']).first()
            print(user.id)
            user_info = Userinfo(id=user.id, email=user.email, interests=None)
            db.session.add(user_info)
            db.session.commit()
            # flash("success register！")
            my_json["message"] = "success register！"
            # create uuid
            user = User.query.filter(and_(User.email == my_json['email'], User.password == my_json['password1'])).first()
            uuid_temp = uuid4().hex
            user.uuid = uuid_temp
            my_json["uuid"] = uuid_temp
            db.session.commit()
            # add to firebase user
            data = {
                'email':user.email,
                'password':user.password,
                'uuid':user.uuid
            }
            add_to_firebase.add_to_user(data,user.id)
            # add to firebase userinfo
            userinfo = Userinfo.query.filter(Userinfo.email == user.email).first()
            data2 = {
                'age':userinfo.age,
                'firstname':userinfo.firstname,
                'lastname':userinfo.lastname,
                'gender':userinfo.gender,
                'interest':userinfo.interests,
                'birthday':userinfo.birthday
            }

            add_to_firebase.add_to_userinfo(data2,userinfo.id)

            return my_json

        my_json["error"] = error
        return my_json

    return render_template('regist.html', error=error)
