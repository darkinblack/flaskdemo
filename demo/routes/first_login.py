from flask import Blueprint, request
from flask import render_template, redirect, url_for, flash, session
from ..models import db
from sqlalchemy import and_, or_
from ..models import User, Userinfo
from functools import wraps
import random
import time
import json
# import gensim.downloader
import pandas as pd
import numpy as np



# define class for better performance
# class keywords:
#     def __init__(self):
#
#         self.data = pd.read_csv("/Users/zhaolunshi/Desktop/flaskdemo/demo/unigram_freq.csv")
#         self.interest = list(self.data['word'])
#         self.vector = gensim.downloader.load('glove-twitter-25')
#
# interest_init = keywords()


class hobby_coff:
    def __init__(self):
        with open('/Users/zhaolunshi/Desktop/flaskdemo/demo/hobby_dic.json') as f:
            self.coff = json.load(f)

hobby_coff = hobby_coff()




first_login = Blueprint('first_login', __name__)

#
def get_interest(n):
    n = n//200

    return "hobby"+str(n)


def get_interests():
    interests = []
    for i in range(random.randint(4, 20)):
        n = random.randint(0, 20000)
        interests.append(get_interest(n))
    out = ''
    for word in interests:
        try:
            out += word + ','
        except:
            pass
    return out

def coff_two_hobby(hobby1,hobby2):
    try:

        return hobby_coff.coff[hobby1][hobby2]
    except:
        return 0


def match_rate(main_user_hobby,target_user_hobby):
    coff = []
    for hobby in main_user_hobby:

        coff.append(max([coff_two_hobby(hobby,hobby2) for hobby2 in target_user_hobby]))

    return np.mean(coff)


@first_login.route('/first_login', methods=['GET', 'POST'])
def first_login_index():
    error = None
    if request.method == 'POST':
        t0 = time.time()

        my_json = request.get_json()

        user_id = my_json["user_id"]
        print(user_id)
        main_user = Userinfo.query.filter(Userinfo.id == user_id).first()
        print(main_user.id)
        main_hobby = main_user.interests.split(",")

        target = Userinfo.query.all()
        best_four = [[0,-1],[0,-1],[0,-1],[0,-1]]
        best_one = [0,-1]
        for people in target:
            target_hobby = people.interests.split(",")
            coff = match_rate(main_hobby,target_hobby)
            print(coff)
            if coff > best_one[1] and people.id != user_id:
                best_one = [people.id,coff]



        return {"ans":best_one}










        # similar_interest = interest_init.vector.most_similar(interest)
        # good_interest = [x for x in similar_interest if x[1]>= 0.80]
        # user_list = {}
        # output = {}
        # output['search_interest'] = interest
        #
        # for each_interest in [(interest,1)]+good_interest:
        #     print(each_interest,type(each_interest))
        #     target = Userinfo.query.filter(Userinfo.interests.like("%" + each_interest[0] + "%")).all()
        #     print(target)
        #     if target:
        #         for people in target:
        #             user_list[people.id] = {'firstname':people.firstname, "lastname":people.lastname, 'interest':each_interest[0], 'coffi':each_interest[1]}
        # output["time"] = str(time.time() - t0)
        # output["user"] = user_list
        return "1"





    elif request.method == 'GET':
        t0 = time.time()
        for i in range(100):
            userinfo = Userinfo(age=i % 30, firstname=str(i) + 'name', lastname=str(i) + 'laname',
                                interests=get_interests())
            db.session.add(userinfo)
            # if i % 1000 == 0:
            #     db.session.commit()
        db.session.commit()

    return str(time.time() - t0)
