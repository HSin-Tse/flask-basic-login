from flask import Blueprint
from flask_restful import Api, Resource

from api.rolo_resources import UserListResource, UserResource

api_bp = Blueprint('api', __name__, 'templates')
api = Api(api_bp)

#
#
#
# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}
#
# api.add_resource(HelloWorld, '/test/hello')


from api.resources import TodoListResource
from api.resources import TodoResource

api.add_resource(TodoListResource, '/todos', endpoint='todos')
api.add_resource(TodoResource, '/todos/<string:id>', endpoint='todo')

api.add_resource(UserListResource, '/users', endpoint='users')
api.add_resource(UserResource, '/users/<string:id>', endpoint='user')
