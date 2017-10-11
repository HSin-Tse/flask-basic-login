from flask import Blueprint

hell = Blueprint('hello', __name__)


@hell.route("/hello")
def hello():
    return "Hello World!"



