from flask import (
    Flask,
    Blueprint,
    flash,

)
from flask_admin import Admin
from sqlalchemy import Column

from admin_helper.adminhelper import MyView

from api.api import api_bp  # module
from extensions import principals, role_admin, role_editor, action_sign_in
from ro.views import hell  # module

from flask_principal import (
    identity_loaded,
)

from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user,current_user

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx')

principals.init_app(app)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
# login_manager.login_view = 'auth.login'
login_manager.login_message = u"请登录！"
login_manager.init_app(app)




# user models
class User(UserMixin):

    name = 'tse'

    def is_authenticated(self):
        return True

    def is_actice(self):
        return True

    def is_anonymous(self):
        return False
    def get_name(self):
        return self.name
    def get_id(self):
        return "1"
    def __repr__(self):
        return '<Role %r>' % self.name

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    user = User()
    # user = load_user(user)

    login_user(user)
    return "login page"


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    flash(u'你已经注销！')
    logout_user()
    return "logout page"

# @login_manager.unauthorized_handler(action_sign_in())
#     def unauthorized():
#         # do stuff
#         return "login unauthorized_handler"

@app.route("/")
# @login_required
def hello():
    return "Hello World! %r" % current_user.get_name()


@login_manager.user_loader
def load_user(user_id):
    print(" user_id:", user_id, '-->File "run.py", line 77')

    user = User()
    return user
    # 以上这段是新增加的============


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    needs = []

    if identity.id in ('the_only_user', 'the_only_editor', 'the_only_admin'):
        needs.append(action_sign_in)

    if identity.id in ('the_only_editor', 'the_only_admin'):
        needs.append(role_editor)

    if identity.id == 'the_only_admin':
        needs.append(role_admin)

    for n in needs:
        identity.provides.add(n)


        return "logout page"


if __name__ == '__main__':
    admin = Admin(app, name='Tse')
    admin.add_view(MyView(name='Hello'))

    app.register_blueprint(hell)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth, url_prefix='/auth')
    app.run(debug=True)
