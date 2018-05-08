# -*- encoding: UTF-8 -*-

import unittest
import logging
from flaskagram import app

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class FlaskagramTest(unittest.TestCase):
    def setUp(self):
        logger.info('setup')
        app.config['TESTING'] = True
        self.app = app.test_client()

    # def setUpClass(cls):
    #     logger.info('setupClass')

    def tearDown(self):
        logger.info('tearDown')
    #
    # def tearDownClass(cls):
    #     logger.info('tearDownClass')

    def register(self, username, password):
        return self.app.post('/register/',
                             data={'username': username,
                                   'password': password},
                             follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/signin/',
                             data={'username': username,
                                   'password': password},
                             follow_redirects=True)

    def logout(self):
        return self.app.get('/logout/')

    def test_reg_login_logout(self):
        logger.info('test_reg_login_logout')
        assert self.register('Test_User', 'Test_Password').status_code == 200
        self.logout()
        assert 'Test_User' not in self.app.open('/').data.decode("utf-8")
        self.login('Test_User', 'Test_Password')
        assert 'Test_User' in self.app.open('/').data.decode("utf-8")

    def test_profile(self):
        logger.info('test_profile')
        r = self.app.open('/profile/3/', follow_redirects=True)
        assert r.status_code == 200
        assert 'password' in r.data.decode("utf-8")
        self.login('Test_User', 'Test_Password')
        assert 'Test_User' in self.app.open('/profile/102/', follow_redirects=True).data.decode('utf-8')