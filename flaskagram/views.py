# -*- encoding: UTF-8 -*-


from flaskagram import app
from flask import render_template, redirect
from flaskagram.models import Image, User


@app.route('/')
def index():
    images = Image.query.order_by('id asc').limit(10).all()
    return render_template('index.html', images=images)


@app.route('/image/<int:image_id>')
def image(image_id):
    image = Image.query.get(image_id)
    if image is None:
        return redirect('/')
    return render_template('page_detail.html', image=image)


@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get(user_id)
    if user is None:
        return redirect('/')
    return render_template('profile.html', user=user)