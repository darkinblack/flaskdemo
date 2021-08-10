from flask import Blueprint, request
from flask import render_template, redirect, url_for, flash, session
from ..models import db
from sqlalchemy import and_, or_
from ..models import User, Userinfo
from functools import wraps
import random
import time
import json
import gensim.downloader
import pandas as pd



# define class for better performance
class keywords:
    def __init__(self):

        self.data = pd.read_csv("/Users/zhaolunshi/Desktop/flaskdemo/demo/unigram_freq.csv")
        self.interest = list(self.data['word'])
        self.vector = gensim.downloader.load('glove-twitter-25')

interest_init = keywords()






search = Blueprint('search', __name__)


def get_interest(n):
    return interest_init.interest[n]


def get_interests():
    interests = []
    for i in range(random.randint(0, 20)):
        n = random.randint(0, 20000)
        interests.append(get_interest(n))
    out = ''
    for word in interests:
        try:
            out += word + ','
        except:
            pass
    return out


@search.route('/search', methods=['GET', 'POST'])
def search_index():
    error = None
    if request.method == 'POST':



        t0 = time.time()

        my_json = request.get_json()

        interest = my_json["interest"]
        print(interest)
        similar_interest = interest_init.vector.most_similar(interest)
        good_interest = [x for x in similar_interest if x[1]>= 0.80]
        user_list = {}
        output = {}
        output['search_interest'] = interest

        for each_interest in [(interest,1)]+good_interest:
            print(each_interest,type(each_interest))
            target = Userinfo.query.filter(Userinfo.interests.like("%" + each_interest[0] + "%")).all()
            print(target)
            if target:
                for people in target:
                    user_list[people.id] = {'firstname':people.firstname, "lastname":people.lastname, 'interest':each_interest[0], 'coffi':each_interest[1]}
        output["time"] = str(time.time() - t0)
        output["user"] = user_list
        return output





    elif request.method == 'GET':
        t0 = time.time()
        for i in range(10000):
            userinfo = Userinfo(age=i % 30, firstname=str(i) + 'name', lastname=str(i) + 'laname',
                                interests=get_interests())
            db.session.add(userinfo)
            if i % 1000 == 0:
                db.session.commit()

    return str(time.time() - t0)
