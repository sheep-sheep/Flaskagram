# -*- encoding: UTF-8 -*-
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('app.conf')
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
db = SQLAlchemy(app)
app.secret_key = 'flaskagram'
login_manager = LoginManager(app)
login_manager.login_view = '/loginpage/'
from flaskagram import views, models