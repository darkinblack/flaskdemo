from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
# from geoalchemy2.types import Geometry
# from sqlalchemy.ext.declarative import declarative_base
# from geoalchemy import *
import sys
import os
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    uuid = db.Column(db.String(80))




    def __repr__(self):
        return '<User %r>' % self.email


class Userinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, ForeignKey("user.id"))
    email = db.Column(db.String(120), unique=True)
    interests = db.Column(db.String(200))
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    birthday = db.Column(db.String(10))
    age = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    # geom = GeometryColumn(Point(2))
    user = relationship("User")


    def __repr__(self):
        return '<Userinfo %r>' % self.email



class Match(db.Model):
    match_id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    start_time = db.Column(db.DateTime)
    ativity = db.Column(db.String(50))
    users = db.Column(db.String(200))

    def __repr__(self):
        return '<Match %r>' % self.match_id



class Interactions(db.Model):
    interaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"))

    start_time = db.Column(db.DateTime)
    ativity = db.Column(db.String(50))

    user = relationship("User")
    def __repr__(self):
        return '<Match %r>' % self.match_id

class Rate(db.Model):
    rate_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"))
    target = db.Column(db.Integer)
    rate = db.Column(db.Integer)




# class UserLocation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     location = db.Column(Geometry('POINT'))
#     email = db.Column(db.String(120), unique=True)
#
#     def __repr__(self):
#         return '<UserLocation %r>' % self.email

