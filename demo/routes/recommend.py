from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import os
import io
from surprise import KNNBaseline
from surprise import Dataset

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a， %d %b %Y %H:%M:%S')

from flask import  Blueprint,request
from flask import  render_template, redirect, url_for, flash, session
from ..models import db
from sqlalchemy import and_, or_
from ..models import User, Userinfo
from functools import wraps

recommend = Blueprint('recommend', __name__)

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # if g.user:
        if session.get('email'):
            return func(*args, **kwargs)
        else:
            return "you havent login" #

    return wrapper



def getSimModle():
    # 默认载入movielens数据集
    data = Dataset.load_builtin('ml-100k')
    trainset = data.build_full_trainset()
    #使用pearson_baseline方式计算相似度  False以item为基准计算相似度 本例为电影之间的相似度
    sim_options = {'name': 'pearson_baseline', 'user_based': False}
    ##使用KNNBaseline算法
    algo = KNNBaseline(sim_options=sim_options)
    #训练模型
    algo.fit(trainset)
    return algo



def read_item_names():
    """
    获取电影名到电影id 和 电影id到电影名的映射
    """
    file_name = (os.path.expanduser('~') +
                 '/.surprise_data/ml-100k/ml-100k/u.item')
    rid_to_name = {}
    name_to_rid = {}
    with io.open(file_name, 'r', encoding='ISO-8859-1') as f:
        for line in f:
            line = line.split('|')
            rid_to_name[line[0]] = line[1]
            name_to_rid[line[1]] = line[0]
    return rid_to_name, name_to_rid


def showSimilarMovies(algo, user_id):
    # 获得电影Toy Story (1995)的raw_id
    toy_story_raw_id = str(user_id)
    print("+++++++"+toy_story_raw_id)
    logging.debug('raw_id=' + toy_story_raw_id)
    #把电影的raw_id转换为模型的内部id
    toy_story_inner_id = algo.trainset.to_inner_iid(toy_story_raw_id)
    logging.debug('inner_id=' + str(toy_story_inner_id))
    #通过模型获取推荐电影 这里设置的是10部
    toy_story_neighbors = algo.get_neighbors(toy_story_inner_id, 10)
    logging.debug('neighbors_ids=' + str(toy_story_neighbors))
    #模型内部id转换为实际电影id
    neighbors_raw_ids = [algo.trainset.to_raw_iid(inner_id) for inner_id in toy_story_neighbors]
    #通过电影id列表 或得电影推荐列表
    # neighbors_movies = [rid_to_name[raw_id] for raw_id in neighbors_raw_ids]
    print('The 10 nearest neighbors of user are:')
    return neighbors_raw_ids[:4]

# rid_to_name, name_to_rid = read_item_names()
algo = getSimModle()

@recommend.route('/recommend', methods=['GET', 'POST'])
# @login_required
def recommend_index():
    my_json = request.get_json()
    uuid_temp = my_json["uuid"]
    user = User.query.filter(User.uuid == uuid_temp).first()
    userinfo = Userinfo.query.filter(Userinfo.email == user.email).first()

    if request.method == 'POST':


        return {"recommend_user" :showSimilarMovies(algo,user.id)}
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
        # return "updated " + str(my_json)
    elif request.method == 'GET':
        try:
            return {'interest': userinfo.interests, 'firstname': userinfo.firstname, 'lastname': userinfo.lastname \
                , 'age': userinfo.age,'uuid':user.uuid}
        except:
            return "error"