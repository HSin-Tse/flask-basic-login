from flask import Flask
# from flask.ext import restful
from ro.views import hell
from api.api import api_bp


app = Flask(__name__)
app.register_blueprint(hell)
app.register_blueprint(api_bp)
# api = restful.Api(app)



# class HelloWorld(restful.Resource):
#     def get(self):
#         return {'hello': 'world'}

# api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.register_blueprint(hell)
    app.register_blueprint(api_bp)
    app.run(debug=True)