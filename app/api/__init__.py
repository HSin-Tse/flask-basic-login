from flask import Blueprint, jsonify
from flask_restful import Api, abort

from app.api.rolo_resources import UserListResource, UserResource

api_bp = Blueprint('api', __name__, 'templates')
api = Api(api_bp)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@api_bp.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@api_bp.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    print(" tasks[task_id]:", tasks[task_id], '-->File "__init__.py", line 32')
    print(" tasks[task_id]:", tasks[task_id], '-->File "__init__.py", line 32')
    print(" tasks[task_id]:", tasks[task_id], '-->File "__init__.py", line 32')
    print(" tasks[task_id]:", tasks[task_id], '-->File "__init__.py", line 32')
    print(" tasks[task_id]:", tasks[task_id], '-->File "__init__.py", line 32')
    print(" tasks[task_id]:", tasks[task_id], '-->File "__init__.py", line 32')



    # print(" task_id:", task_id, '-->File "__init__.py", line 32')
    # print(" task_id:", task_id, '-->File "__init__.py", line 32')
    # print(" task_id:", task_id, '-->File "__init__.py", line 32')
    # print(" task_id:", task_id, '-->File "__init__.py", line 32')
    # print(" task_id:", task_id, '-->File "__init__.py", line 32')
    # print(" task_id:", task_id, '-->File "__init__.py", line 32')
    #
    # task = filter(lambda t: t['id'] == task_id, tasks)
    #
    # if len(task) == 0:
    #     abort(404)
    return jsonify({'task': tasks[task_id]})


#
#
#
# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}
#
# api.add_resource(HelloWorld, '/test/hello')


# from app.api.resources import TodoListResource
# from app.api.resources import TodoResource

# api.add_resource(TodoListResource, '/todos', endpoint='todos')
# api.add_resource(TodoResource, '/todos/<string:id>', endpoint='todo')

api.add_resource(UserListResource, '/users', endpoint='users')
api.add_resource(UserResource, '/users/<string:id>', endpoint='user')
