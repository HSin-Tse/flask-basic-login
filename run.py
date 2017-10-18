import os

from flask_admin import Admin

from app import create_app
from app.controllers.admin import CustomFileAdmin, MyView
from db_sessions import session_roles, session_roles_aj

# from roles import User, Role

app = create_app('config')
from extensions import db

# app.config.update(
#     DEBUG=True,
#     SECRET_KEY='secret_xxx')

from flask_admin.contrib.sqla import ModelView

admin = Admin(app, name='Tse')
admin.add_view(MyView(name='Hello'))
# admin.add_view(ModelView(User, session_roles))
# admin.add_view(ModelView(Role, session_roles))

from app.admodels import  Role, User

admin.add_view(ModelView(Role, session_roles_aj))
admin.add_view(ModelView(User, session_roles_aj))

basedir = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(basedir, 'app', 'static')
admin.add_view(CustomFileAdmin(path,
                               '/static',
                               name='Static Files'))
if __name__ == '__main__':

    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])
