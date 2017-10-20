import os

import time
from flask_admin import Admin

from app import create_app
from app.controllers.admin import CustomFileAdmin, MyView
from db_sessions import session_roles_aj

from flask_admin.contrib.sqla import ModelView
from app.admodels import Role, User

app = create_app('config')

admin = Admin(app, name='Tse')
admin.add_view(MyView(name='Hello'))

admin.add_view(ModelView(Role, session_roles_aj))
admin.add_view(ModelView(User, session_roles_aj))

basedir = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(basedir, 'app', 'static')
admin.add_view(CustomFileAdmin(path,
                               '/static',
                               name='Static Files'))

from flask_mail import Mail, Message


app.config.update(
    MAIL_SERVER='smtp.partner.outlook.cn',
    MAIL_PORT=587,
    # MAIL_USE_TTLS=True,
    MAIL_USE_TLS=True,
    MAIL_DEFAULT_SENDER=os.environ.get('MAIL_USERNAME'),
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
)
mail = Mail()

mail.init_app(app)


@app.route('/')
def send_mail():
    msg = Message(subject="Hello",
                  recipients=['2481640274@qq.com']
                  )

    msg.html = '<h1>Hello World</h1>'
    mail.send(msg)
    return 'Successful'


if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])
