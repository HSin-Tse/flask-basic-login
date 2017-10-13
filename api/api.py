from flask import Blueprint
from flask_restful import Api, Resource

api_bp = Blueprint('api', __name__, 'templates')
api = Api(api_bp)




class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/test/hello')


from api.resources import TodoListResource
from api.resources import TodoResource

api.add_resource(TodoListResource, '/todos', endpoint='todos')
api.add_resource(TodoResource, '/todos/<string:id>', endpoint='todo')