# -*- encoding: UTF-8 -*-
import hashlib
import json

from flaskagram import app, db
from flask import render_template, redirect, request, flash, get_flashed_messages
from flaskagram.models import Image, User
from flask_login import login_user, logout_user, current_user, login_required
import random


@app.route('/')
def index():
    images = Image.query.order_by('id').limit(10).all()
    return render_template('index.html', images=images)


@app.route('/image/<int:image_id>')
def image(image_id):
    image = Image.query.get(image_id)
    if image is None:
        return redirect('/')
    return render_template('page_detail.html', image=image)


@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if user is None:
        return redirect('/')
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=1, per_page=3, error_out=False)
    return render_template('profile.html', user=user, images=paginate.items, has_next=paginate.has_next )


@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_images(user_id, page, per_page):
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    images = []
    for image in paginate.items:
        image_info = {'id': image.id,
                      'url': image.url,
                      'comment_count': len(image.comments)}
        images.append(image_info)

    map = {'has_next':paginate.has_next,
           'images': images}
    return json.dumps(map)


@app.route('/loginpage/')
def loginpage():
    # decode the msg and display it on webpage
    # support next redirect
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['register']):
        msg += m
    return render_template('login.html', msg=msg, next=request.values.get('next'))


@app.route('/signin/', methods=['post', 'get'])
def signin():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    user = User.query.filter_by(username=username).first()
    if user is None:
        # add additional message and go to the new page
        return redirect_with_msg('/loginpage/', 'The username hasn\'t been registered.', 'register')
    m = hashlib.md5()
    m.update((password+user.salt).encode('utf-8'))
    if m.hexdigest() != user.password:
        return redirect_with_msg('/loginpage/', 'Password is incorrect', 'register')

    login_user(user)
    next_papge = request.values.get('next')
    if next_papge is not None and next_papge.startswith('/'):
        return redirect(next_papge)
    return redirect('/')


def redirect_with_msg(target, msg, category):
    if msg is not None:
        flash(msg, category)
        return redirect(target)


@app.route('/register/', methods=['post', 'get'])
def register():
    # request.args
    # request.form
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    if username in ('admin', '', 'root'):
        return redirect_with_msg('/loginpage/', 'Invalid Username', 'register')

    user = User.query.filter_by(username=username).first()
    if user is not None:
        # add additional message and go to the new page
        return redirect_with_msg('/loginpage/', 'The username has been registered.', 'register')

    salt = ''.join(random.sample('ABCDEFGHIJKmlnopqrstuvwxyz1234567890', 5))
    m = hashlib.md5()
    m.update((password + salt).encode('utf-8'))
    password = m.hexdigest()
    user = User(username, password, salt)
    db.session.add(user)
    db.session.commit()

    # login automatically after sign up
    login_user(user)
    next_papge = request.values.get('next')
    if next_papge is not None and next_papge.startswith('/'):
        return redirect(next_papge)
    return redirect('/')


@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')


