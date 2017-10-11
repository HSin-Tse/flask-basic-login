from flask import Flask
from flask.ext import restful
from ro.views import hell
from api.api import api_bp

from flask_admin import Admin, BaseView, expose

app = Flask(__name__)
# app.register_blueprint(hell)
# app.register_blueprint(api_bp)
# api = restful.Api(app)

class MyView(BaseView):
    @expose('/')
    def index(self):
        return "aaaa"

class HelloWorld(restful.Resource):
    def get(self):
        return {'hello': 'world'}

# api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    admin = Admin(app, name='My App')
    admin.add_view(MyView(name='Hello'))
    app.register_blueprint(hell)
    app.register_blueprint(api_bp)
    app.run(debug=True)