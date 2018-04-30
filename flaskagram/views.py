# -*- encoding: UTF-8 -*-


from flaskagram import app
from flask import render_template

from flaskagram.models import Image, User


@app.route('/')
def index():
    images = Image.query.order_by('id asc').limit(10).all()
    return render_template('index.html', images=images)
