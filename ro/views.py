from flask import Blueprint, render_template

from db import session_roles
# from extensions import role_admin
from extensions import role_admin, admin_permission, user_permission
from roles import User, Role


hell = Blueprint('hello', __name__, 'templates')


@hell.route("/hello")
@admin_permission.require(http_exception=403)

def hello():
    return "Hello World!"


@hell.route('/hoeee')

def ssss():
    return render_template('test.html')


# test
@hell.route('/test')
@user_permission.require(http_exception=403)
def home():
    return render_template('test.html', roles=session_roles.query(Role).all(), users=session_roles.query(User).all(),
                           tse=session_roles.query(User).filter_by(username='tse').all()[0].role.name == 'admin')
