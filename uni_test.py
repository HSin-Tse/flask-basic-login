from flask import Flask
from flask_testing import TestCase

from app import create_app


class MyTest(TestCase):

    def create_app(self):

        app = create_app('config')
        app.config['TESTING'] = True
        return app