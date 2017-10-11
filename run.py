from flask import Flask, Blueprint
from ro.views import hell  # module
from api.api import api_bp  # module

from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin
from flask_admin import Admin, BaseView, expose
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)




app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sample_db.sqlite'

app.config['SQLALCHEMY_ECHO'] = True

b = SQLAlchemy(app)
db = SQLAlchemy(app)


class UserDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


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
    return "yes , you are allowed" + app.config['SQLALCHEMY_DATABASE_URI']


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
    from resources import TodoListResource
    from resources import TodoResource

    api = Api(app)
    api.add_resource(TodoListResource, '/todos', endpoint='todos')
    api.add_resource(TodoResource, '/todos/<string:id>', endpoint='todo')


    admin = Admin(app, name='My App')
    admin.add_view(MyView(name='Hello'))



    app.register_blueprint(hell)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_b)

    # if not os.path.exists('db.sqlite'):
    # db.create_all()

    app.run(debug=True)
