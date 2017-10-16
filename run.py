from flask import (
    Blueprint,
    flash,
    render_template,

)
from flask_admin import Admin

from admin_helper.adminhelper import MyView

from db import session_roles

from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user, current_user, login_manager

from roles import User, Role
from app import create_app

app = create_app('config')

app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx')

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    user = session_roles.query(User).first()
    print(" user get_username:", user.get_username(), '-->File "run.py", line 67')
    print(" user:", user.id, '-->File "run.py", line 67')
    # load_user(user)

    login_user(user, True)
    return "login page user.id %r " % user.id


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    flash(u'你已经注销！')
    logout_user()
    return "logout page"


@app.route("/")
# @login_required
def hello():
    print(" current_user:", current_user, '-->File "run.py", line 93')

    return "Hello World! %r" % current_user.username


@app.route("/lll")
def wwwww():
    return render_template('test.html', tse=current_user.role)


from flask_admin.contrib.sqla import ModelView

admin = Admin(app, name='Tse')
admin.add_view(MyView(name='Hello'))
admin.add_view(ModelView(User, session_roles))
admin.add_view(ModelView(Role, session_roles))

app.register_blueprint(auth, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)
