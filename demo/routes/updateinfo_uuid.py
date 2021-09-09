from flask import  Blueprint,request
from flask import  render_template, redirect, url_for, flash, session
from ..models import db
from sqlalchemy import and_, or_
from ..models import User, Userinfo
from functools import wraps

updateinfo_uuid = Blueprint('updateinfo_uuid', __name__)

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # if g.user:
        if session.get('email'):
            return func(*args, **kwargs)
        else:
            return "you havent login" #

    return wrapper

@updateinfo_uuid.route('/updateinfo_uuid', methods=['GET', 'POST'])
# @login_required
def updateinfo_uuid_index():
    my_json = request.get_json()
    uuid_temp = my_json["uuid"]
    user = User.query.filter(User.uuid == uuid_temp).first()
    userinfo = Userinfo.query.filter(Userinfo.email == user.email).first()
    # http post method. But keyword type can be get or update.
    if request.method == 'POST':
        # get to get info
        if my_json["type"] == "get":
            try:
                return {'interest': userinfo.interests, 'firstname': userinfo.firstname, 'lastname': userinfo.lastname \
                    , 'age': userinfo.age, 'uuid': user.uuid,'gender': userinfo.gender, 'birthday': userinfo.birthday}
            except:
                return "error"
        # update to update info
        elif my_json["type"] == "update":

            # update  do not need to have them all
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
            try:
                userinfo.gender = my_json['gender']
            except:
                pass
            try:
                userinfo.birthday = my_json['birthday']
            except:
                pass

            db.session.commit()
            my_json["result"] = "updated"
        return  my_json
    # should not be active
    elif request.method == 'GET':

        return "error"