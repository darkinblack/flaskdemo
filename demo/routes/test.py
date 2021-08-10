from flask import  Blueprint
from ..models import db

from ..models import User

test = Blueprint('test', __name__)



@test.route('/test')
def test_index():
    user = User(password='password1', email='1@1.com')
    db.session.add(user)
    db.session.commit()

    user = User.query.filter(User.email == 'admin@example.com').first()


    return "hello blueprint test"+user.password
