from flask_admin import Admin

from admin_helper.adminhelper import MyView

from db import session_roles

from roles import User, Role
from app import create_app

app = create_app('config')

app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx')

from flask_admin.contrib.sqla import ModelView

admin = Admin(app, name='Tse')
admin.add_view(MyView(name='Hello'))
admin.add_view(ModelView(User, session_roles))
admin.add_view(ModelView(Role, session_roles))

if __name__ == '__main__':
    app.run(debug=True)
