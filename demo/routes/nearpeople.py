from flask import  Blueprint,request
from flask import  render_template, redirect, url_for, flash, session
from ..models import db
from sqlalchemy import and_, or_
from ..models import User, Userinfo
from functools import wraps
# from haversine import haversine, Unit
import random

nearpeople = Blueprint('nearpeople', __name__)

def random_location():
    n = random.randint(-500000, 500000)/100000
    m = random.randint(-500000, 500000)/100000
    return 41+n,-74+m







def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # if g.user:
        if session.get('email'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login', next=request.url))  #

    return wrapper

@nearpeople.route('/nearpeople', methods=['GET', 'POST'])

def nearpeople_index():

    email = session.get('email')
    user = User.query.filter(User.email == email).first()
    userinfo = Userinfo.query.filter(Userinfo.email == email).first()
    my_json = request.get_json()
    if request.method == 'POST':


        my_json = request.get_json()
        longtitude = my_json["lon"]
        latitude = my_json["lat"]
        top = my_json["top"]
        bottom = my_json["bottom"]
        left = my_json["left"]
        right = my_json["right"]
        center = (latitude,longtitude)
        print(longtitude,latitude)


        user_list = {}
        output = {}
        output['center of circle'] = [longtitude,latitude]
        target = Userinfo.query.filter(and_(Userinfo.lon > left, Userinfo.lon <right,\
                                            Userinfo.lat>bottom,Userinfo.lat<top)).all()
        # target = Userinfo.query.filter(and_(Userinfo.lon > -74,Userinfo.lon <-72)).all()
        if target:
            print("1")
            for people in target:
                user_list[people.id] = {'firstname': people.firstname, "lastname": people.lastname,
                                            'lon': people.lon, 'lat': people.lat}





        # for each_interest in [(interest, 1)] + good_interest:
        #     print(each_interest, type(each_interest))
        #     target = Userinfo.query.filter(Userinfo.interests.like("%" + each_interest[0] + "%")).all()
        #     print(target)
        #     if target:
        #         for people in target:
        #             user_list[people.id] = {'firstname': people.firstname, "lastname": people.lastname,
        #                                     'interest': each_interest[0], 'coffi': each_interest[1]}
        # output["time"] = str(time.time() - t0)
        output["user"] = user_list
        return output


    elif request.method == 'GET':

        for i in range(100):
            latitude,longtitude = random_location()
            userinfo = Userinfo(age=i % 30, firstname=str(i) + 'name', lastname=str(i) + 'laname',
                                lon = longtitude,lat = latitude)
            db.session.add(userinfo)
            # if i % 1000 == 0:
            db.session.commit()
        return "random people added"