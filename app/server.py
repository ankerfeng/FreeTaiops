#!/usr/bin/env python
#coding:utf8

import os
import sys
from flask import Flask
from common.modles import UserModel, db
from flask import Flask
from flask.ext.login import LoginManager
from common.config import config
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)


    from auth.inc import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from main.inc import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from appinfo.views import appinfo as appinfo_blueprint
    app.register_blueprint(appinfo_blueprint)

    return app

if __name__ == '__main__':
    model = None
    try:
        model = sys.argv[1]
    except:
        pass
    app = create_app(model or 'default')
    app.run(host='127.0.0.1')