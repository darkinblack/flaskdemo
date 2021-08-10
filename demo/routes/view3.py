from flask import  Blueprint
main3 = Blueprint('main3', __name__)

@main3.route('/new3')
def main3_index():
    return "hello blueprint3"
