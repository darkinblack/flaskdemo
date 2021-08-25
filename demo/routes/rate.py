from flask import Blueprint, request
from flask import render_template, redirect, url_for, flash, session
from ..models import db
from sqlalchemy import and_, or_
from ..models import User, Userinfo, Rate
from functools import wraps

rate = Blueprint('rate', __name__)


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # if g.user:
        if session.get('email'):
            return func(*args, **kwargs)
        else:
            return "you havent login"  #

    return wrapper


@rate.route('/rate', methods=['GET', 'POST'])
# @login_required
def rate_index():
    my_json = request.get_json()
    uuid_temp = my_json["uuid"]
    user = User.query.filter(User.uuid == uuid_temp).first()
    userinfo = Userinfo.query.filter(Userinfo.email == user.email).first()

    if request.method == 'POST':
        # if my_json["type"] == "get":
        #     try:
        #         return {'interest': userinfo.interests, 'firstname': userinfo.firstname, 'lastname': userinfo.lastname \
        #             , 'age': userinfo.age, 'uuid': user.uuid}
        #     except:
        #         return "error"
        # elif my_json["type"] == "update":
        #
        #
        #
        #
        #     try:
        #         userinfo.interests = my_json['interests']
        #     except:
        #         pass
        #     try:
        #         userinfo.firstname = my_json['firstname']
        #     except:
        #         pass
        #     try:
        #         userinfo.lastname = my_json['lastname']
        #     except:
        #         pass
        #     try:
        #         userinfo.age = my_json['age']
        #     except:
        #         pass
        #     db.session.commit()
        if my_json["type"] == "update":
            rate = Rate(user_id=user.id, target=my_json['target'], rate=my_json["rate"])
            db.session.add(rate)
            db.session.commit()
            return "add rate"
        elif my_json["type"] == "get":
            rate = Rate.query.filter(Rate.user_id == User.id).all()
            rate_user = {}
            for each_rate in rate:
                rate_user[each_rate.target] = each_rate.rate

            return rate_user
    elif request.method == 'GET':
        return "wait"




