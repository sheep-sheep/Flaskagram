# -*- encoding: UTF-8 -*-
import datetime

from flaskagram import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32))
    avatar_url = db.Column(db.String(256))
    images = db.relationship('Image', backref='user', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.avatar_url = 'http://www.facets.la/fullview/F_2014_363.jpg'

    def __repr__(self):
        return '<User %d %s>'%(self.id, self.username)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(512))
    created_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments =db.relationship('Comment')

    def __init__(self, url, user_id):
        self.url = url
        self.user_id = user_id
        self.created_time = datetime.datetime.now()

    def __repr__(self):
        return '<Image %d %s>'%(self.id, self.url)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(1024))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Integer, default=0)  # 0 Normal, 1 Deleted
    user = db.relationship('User')
    created_time = db.Column(db.DateTime)

    def __init__(self, comment, image_id, user_id):
        self.comment = comment
        self.image_id = image_id
        self.user_id = user_id
        self.created_time = datetime.datetime.now()

    def __repr__(self):
        return '<Comment %d %s>'%(self.id, self.comment)