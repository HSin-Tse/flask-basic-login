import os

from flask_admin import Admin

from app import create_app
from app.controllers.admin import CustomFileAdmin, MyView, UserView, CustomModelView
from db_sessions import session_roles_aj

from flask_admin.contrib.sqla import ModelView
from app.admodels import Role, User
# from extensions import mail
from flask_mail import Message

from extensions import mail

app = create_app('config.BaseConfig')
# app = create_app('config.DevelopmentConfig')

admin = Admin(app, name='Tse')
# admin.add_view(MyView(name='Hello'))

admin.add_view(ModelView(Role, session_roles_aj))
# admin.add_view(ModelView(User, session_roles_aj))
admin.add_view(UserView(User, session_roles_aj))
# admin.add_view(UserView(User, session_roles_aj))

basedir = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(basedir, 'app', 'static')
admin.add_view(CustomFileAdmin(path,
                               '/static',
                               name='Static Files'))


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


@app.route('/')
def aa():
    return 'home'


if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])
