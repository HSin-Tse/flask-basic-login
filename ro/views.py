from flask import Blueprint,render_template

hell = Blueprint('hello', __name__)


@hell.route("/hello")
def hello():
    return "Hello World!"


#
# @hell.route('/')
# def home():
#     return render_template('test.html')


# # test
# @app.route('/')
# @user.require(http_exception=403)
# def home():
#     return render_template('test.html', roles=session_roles.query(Role).all(), users=session_roles.query(User).all(),
#                            tse=session_roles.query(User).filter_by(username='tse').all()[0].role.name == 'admin')
