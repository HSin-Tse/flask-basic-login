from extensions import user_permission, admin_permission
from db_sessions import session_roles_aj

from flask_restful import reqparse, abort, Resource, fields, marshal_with

from roles import User

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'password': fields.String,
    'uri': fields.Url('api.user', absolute=True),
}

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)


class UserResource(Resource):
    @admin_permission.require(http_exception=403)
    @marshal_with(user_fields)
    def get(self, id):
        todo = session_roles_aj.query(User).filter(User.id == id).first()
        if not todo:
            abort(404, message="Todo {} doesn't exist".format(id))
        return todo

    # @user_permission.require(http_exception=403)
    def delete(self, id):
        todo = session_roles_aj.query(User).filter(User.id == id).first()
        if not todo:
            abort(404, message="Todo {} doesn't exist".format(id))
        session_roles_aj.delete(todo)
        session_roles_aj.commit()
        return {}, 204

    @marshal_with(user_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        todo = session_roles_aj.query(User).filter(User.id == id).first()
        todo.task = parsed_args['task']
        session_roles_aj.add(todo)
        session_roles_aj.commit()
        return todo, 201


class UserListResource(Resource):
    @marshal_with(user_fields)
    @admin_permission.require(http_exception=403)

    def get(self):
        todos = session_roles_aj.query(User).all()
        return todos

    @marshal_with(user_fields)
    def post(self):
        parsed_args = parser.parse_args()
        input_username = parsed_args['username']
        print(" input_username:", input_username, '-->File "rolo_resources.py", line 63')

        tell = session_roles_aj.query(User).filter(User.username == input_username).first()
        if tell is not None:
            return tell

        todo = User(password=parsed_args['password'], username=parsed_args['username'])
        session_roles_aj.add(todo)

        # session_roles.commit()
        try:
            session_roles_aj.commit()
        except:
            session_roles_aj.rollback()

        return todo, 201
