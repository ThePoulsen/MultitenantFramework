## -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, g, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_htmlmin import HTMLMIN
import flask_sijax
import os

# Set unicode encoding
import sys
if sys.version_info.major < 3:
    reload(sys)
sys.setdefaultencoding('utf8')

# Setup Flask and read config from ConfigClass defined above
app = Flask(__name__)
app.config.from_object('config')

# Initialize Flask extensions
# Flask-SQLAlchemy
db = SQLAlchemy(app)

# Flask-mail
mail = Mail(app)

# Flask-sijax
flask_sijax.Sijax(app)

# HTML min
#HTMLMIN(app)

## Import models
from app.admin.models import *

## import blueprints
from app.admin.views import adminBP
from app.auth.views import authBP
from app.settings.views import settingsBP
from app.user.views import userBP

## Register blueprints
app.register_blueprint(adminBP, url_prefix='/admin')
app.register_blueprint(authBP, url_prefix='/auth')
app.register_blueprint(settingsBP, url_prefix='/settings')
app.register_blueprint(userBP, url_prefix='/usr')


# indexView
@app.route('/')
def indexView():
    kwargs = {'title':'Index',
              'contentTitle': '',}
    return render_template('index.html', **kwargs)
