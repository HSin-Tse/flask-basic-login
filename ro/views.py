from flask import Blueprint,render_template

hell = Blueprint('hello', __name__)


@hell.route("/hello")
def hello():
    return "Hello World!"


#
# @hell.route('/')
# def home():
#     return render_template('test.html')
