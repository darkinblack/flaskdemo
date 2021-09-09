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


# add dictionary
def getSimModle():
    # add data
    data = Dataset.load_builtin('ml-100k')
    trainset = data.build_full_trainset()
    # pearson_baseline
    sim_options = {'name': 'pearson_baseline', 'user_based': False}
    ## KNNBaseline to compute
    algo = KNNBaseline(sim_options=sim_options)
    # train model
    algo.fit(trainset)
    return algo



def read_item_names():
    """
    
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
    
    toy_story_raw_id = str(user_id)
    print("+++++++"+toy_story_raw_id)
    logging.debug('raw_id=' + toy_story_raw_id)
    # useless now
    toy_story_inner_id = algo.trainset.to_inner_iid(toy_story_raw_id)
    logging.debug('inner_id=' + str(toy_story_inner_id))
    # get 10 best neighbors
    toy_story_neighbors = algo.get_neighbors(toy_story_inner_id, 10)
    logging.debug('neighbors_ids=' + str(toy_story_neighbors))
    # useless now
    neighbors_raw_ids = [algo.trainset.to_raw_iid(inner_id) for inner_id in toy_story_neighbors]
    # return the 
    # neighbors_movies = [rid_to_name[raw_id] for raw_id in neighbors_raw_ids]
    # print('The 4 nearest neighbors of user are:')
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

        # find most like people with movie data
        return {"recommend_user" :showSimilarMovies(algo,user.id)}
    # not working
    elif request.method == 'GET':
        try:
            return {'interest': userinfo.interests, 'firstname': userinfo.firstname, 'lastname': userinfo.lastname \
                , 'age': userinfo.age,'uuid':user.uuid}
        except:
            return "error"
