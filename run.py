import os

from flask_admin import Admin

from app import create_app
from app.controllers.admin import CustomFileAdmin, MyView
from db import session_roles
from roles import User, Role

app = create_app('config')

app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx')

from flask_admin.contrib.sqla import ModelView

admin = Admin(app, name='Tse')
admin.add_view(MyView(name='Hello'))
admin.add_view(ModelView(User, session_roles))
admin.add_view(ModelView(Role, session_roles))
basedir = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(basedir, 'app', 'static')
admin.add_view(CustomFileAdmin(path,
                               '/static',
                               name='Static Files'))
if __name__ == '__main__':
    app.run(debug=True)
