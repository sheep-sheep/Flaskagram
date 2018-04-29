# -*- encoding: UTF-8 -*-
import random

from flaskagram import app, db
from flask_script import Manager

from flaskagram.models import User, Image, Comment

manager = Manager(app)

urls = ['http://static.simpledesktops.com/uploads/desktops/2014/10/28/Yosemite.png',
        'http://static.simpledesktops.com/uploads/desktops/2014/09/22/keyboard_2880x1800.png',
        'http://static.simpledesktops.com/uploads/desktops/2014/09/02/pulsarmap.png',
        'http://static.simpledesktops.com/uploads/desktops/2014/08/20/Maverick.png',
        'http://static.simpledesktops.com/uploads/desktops/2014/07/23/Pusteblume.png',
        ]


@manager.command
def _init_database():
    # this method should also check permission
    # this should also run merely
    db.drop_all()
    db.create_all()


@manager.command
def _test_create_users():
    for i in range(100):
        db.session.add(User('User'+str(i), 'password'))
        for j in range(3):
            db.session.add(Image(urls[random.randint(0,3)], i+1))
            for k in range(3):
                db.session.add(Comment('I like it very much!', j+1))
    db.session.commit()


if __name__ == '__main__':
    manager.run()