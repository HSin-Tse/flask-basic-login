from flask import Blueprint
from flask_restful import Api, Resource, url_for


api_bp = Blueprint('api', __name__)
api = Api(api_bp)




class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/abc')