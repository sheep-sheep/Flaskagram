# -*- encoding: UTF-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Environment

app = Flask(__name__)
app.config.from_pyfile('app.conf')
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
db = SQLAlchemy(app)

from flaskagram import views, models