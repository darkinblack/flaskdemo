from flask import Flask, Blueprint

from .routes import main3, test, register, login, logout,\
    updateinfo,updatelocation,nearpeople,first_login,login_uuid,updateinfo_uuid,home,rate,recommend
from .models import db
from .models import User
import sys
import os



def creat_app(config_file = "settings.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    WIN = sys.platform.startswith("win")
    if WIN:
        prefix = 'sqlite:///'
    else:
        prefix = 'sqlite:////'


    app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = '\xc9ixnRb\xe40\xd4\xa5\x7f\x03\xd0y6\x01\x1f\x96\xeao+\x8a\x9f\xe4'

    db.init_app(app)

    @app.before_first_request
    def create_db():
        db.drop_all()  # 每次运行，先删除再创建
        db.create_all()

        admin = User(password='root', email='admin@example.com')

        db.session.add(admin)

        db.session.commit()

    # @app.before_first_request
    # def create_db():
    #     db.drop_all()  # 每次运行，先删除再创建
    #     db.create_all()
    #
    #     admin = User(password='root', email='admin@example.com')
    #
    #     db.session.add(admin)
    #
    #     db.session.commit()


    app.register_blueprint(main3)
    app.register_blueprint(test)
    app.register_blueprint(register)
    app.register_blueprint(login)
    app.register_blueprint(logout)
    app.register_blueprint(updateinfo)
    # app.register_blueprint(search)
    app.register_blueprint(updatelocation)
    app.register_blueprint(nearpeople)
    app.register_blueprint(first_login)
    app.register_blueprint(login_uuid)
    app.register_blueprint(updateinfo_uuid)
    app.register_blueprint(home)
    app.register_blueprint(rate)
    app.register_blueprint(recommend)
    return app






