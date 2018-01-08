import os
from contextlib import closing

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
from flask import stream_with_context
from flask import Response

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
    # url = request.url
    # print(" url:", url, '-->File "run.py", line 56')

    # print(" OOO request:",  request, '-->File "run.py", line 56')


    # print(" request.url_root:", request.url_root, '-->File "run.py", line 55')

    # print(" ip:", ip, '-->File "run.py", line 53')
    # print(" url:", url, '-->File "run.py", line 54')


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

    conver_r = eval(bytes.decode(result.content))  ##进行一些类型转化
    print(" json.dumps(conver_r):", json.dumps(conver_r), '-->File "run.py", line 102')

    return json.dumps(conver_r), 200


@app.errorhandler(401)
def authentication_failed(e):
    flash('Authenticated failed.')
    return redirect(url_for('account.login'))


@app.errorhandler(403)
def authorisation_failed(e):
    return (
        ('Your current identity is: {id}.    | who You Are: {who}').format(id=g.identity.id, who=g.identity.provides))


@app.route('/<path:url>', methods=['GET', 'POST'])
def home(url):
    # http: // a.ajmide.com
    # http: // a.ajmide.com / get_history_list.php?type = 0 & i = 0 & c = 20
    # http: // a.ajmide.com / v14 / getMainAudioCate.php



    # print(" request.url,:", request.url, '-->File "run.py", line 134')
    # print(" request.method:", request.method, '-->File "run.py", line 138')
    # print(" request.method:", request.method, '-->File "run.py", line 138')
    # print(" request.method:", request.method, '-->File "run.py", line 138')
    # print(" request.method:", request.method, '-->File "run.py", line 138')
    # print(" request.headers:", request.headers, '-->File "run.py", line 138')
    # print(" request.get_data():", request.get_data(), '-->File "run.py", line 139')
    # print(" request.cookies:", request.cookies, '-->File "run.py", line 140')

    # url = "url%s"
    # print(" request.param:", request.params, '-->File "run.py", line 147')
    # print(" request.param:", request.params, '-->File "run.py", line 147')
    # print(" request.param:", request.params, '-->File "run.py", line 147')

    # req = requests.get(url ,stream = True)
    # param = request.param,


    with closing(

            requests.request(
                method=request.method,
                url=request.url,
                headers=request.headers,
                data=request.get_data(),
                cookies=request.cookies,
                allow_redirects=False)
    ) as resp:
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response

        # request
    # return Response(stream_with_context(req.iter_content()), content_type = req.headers['content-type'])


if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])
