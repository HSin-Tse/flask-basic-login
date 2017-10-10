from flask import Blueprint

hell = Blueprint('hello', __name__)


@hell.route("/")
def hello():
    return "Hello World!"



