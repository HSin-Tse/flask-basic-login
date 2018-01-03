import os
import requests
from flask import (
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    current_app,
    url_for, jsonify)
from flask import flash
from flask_admin import Admin
from flask_principal import ActionNeed, Permission
from flask_restful.representations import json

from app import create_app
from app.controllers.admin import CustomFileAdmin, MyView, UserView, CustomModelView, ChildServiceModol, RoleModol, \
    ActionModol
from db_sessions import session_roles_aj

from flask_admin.contrib.sqla import ModelView
from app.admodels import Role, User, ChildService, Action
# from app.admodels import ChildService, Action
# from extensions import mail
from flask_mail import Message
from flask import request
from extensions import mail, admin_permission, super_permission, cache

app = create_app('config.BaseConfig')
# app = create_app('config.DevelopmentConfig')

admin = Admin(app, name='Tse')
admin.add_view(MyView(name='API'))

admin.add_view(UserView(User, session_roles_aj))
admin.add_view(RoleModol(Role, session_roles_aj))

admin.add_view(ChildServiceModol(ChildService, session_roles_aj))
admin.add_view(ActionModol(Action, session_roles_aj))

basedir = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(basedir, 'app', 'static')
admin.add_view(CustomFileAdmin(path,
                               '/static',
                               name='Static Files'))


@app.before_request
def before_request():
    ip = request.remote_addr
    url = request.url
    print(" ip:", ip, '-->File "run.py", line 53')
    print(" url:", url, '-->File "run.py", line 54')


@app.route('/testmail')
def send_mail():
    mail.init_app(app)

    msg = Message(subject="Hello",
                  # sender=app.config['MAIL_DEFAULT_SENDER'],
                  # sender=['2481640274@qq.com'],
                  recipients=['2481640274@qq.com'],
                  )

    msg.html = '<h1>Hello World</h1>'
    mail.send(msg)
    return 'Successful'


@app.route('/who')
def who():
    return (
        ('Your current identity is: {id}.    | who You Are: {who}').format(id=g.identity.id, who=g.identity.provides))


# @cache.cached(timeout=0)
@app.route('/')
def aa():
    return render_template('account/test.html')


@app.route('/h5')
def testh5():
    return render_template('account/h5static.html')


@app.route('/r')
def r():
    session_roles_aj.rollback()

    return 'home'


@app.route('/proxy', methods=['GET'])
def getTasks():
    result = requests.get('https://c.y.qq.com/musichall/fcgi-bin/fcg_yqqhomepagerecommend.fcg')  ## 请求转发
    print(" result:", result, '-->File "run.py", line 100')
    
    conver_r = eval(bytes.decode(result.content))  ##进行一些类型转化

    return json.dumps(conver_r), 200


@app.errorhandler(401)
def authentication_failed(e):
    flash('Authenticated failed.')
    return redirect(url_for('account.login'))


@app.errorhandler(403)
def authorisation_failed(e):
    return (
        ('Your current identity is: {id}.    | who You Are: {who}').format(id=g.identity.id, who=g.identity.provides))


if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])
