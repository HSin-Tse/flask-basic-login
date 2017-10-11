from flask import Flask, Blueprint
from flask.ext import restful
from ro.views import hell
from api.api import api_bp
from flask.ext.login import LoginManager, login_required, login_user,logout_user, UserMixin
from flask_admin import Admin, BaseView, expose

app = Flask(__name__)
# app.register_blueprint(hell)
# app.register_blueprint(api_bp)
# api = restful.Api(app)

# 以下这段是新增加的============
app.secret_key = 's3cr3t'
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
login_manager.login_message = u"请登录！"

# user models
class User(UserMixin):
    def is_authenticated(self):
        return True

    def is_actice(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return "1"

@login_manager.user_loader
def load_user(user_id):
    user = User()
    return user

@app.route('/test')
@login_required
def test():
    return "yes , you are allowed"

auth_b = Blueprint('auth', __name__)


@auth_b.route('/login', methods=['GET', 'POST'])
def login():
    user = User()
    login_user(user)
    return "login page"


@auth_b.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return "logout page     OUT"


class MyView(BaseView):
    @expose('/')
    def index(self):
        return "aaaa"

if __name__ == '__main__':
    admin = Admin(app, name='My App')
    admin.add_view(MyView(name='Hello'))
    app.register_blueprint(hell)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_b)
    app.run(debug=True)