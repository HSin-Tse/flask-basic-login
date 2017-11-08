from flask import request

from extensions import user_permission, admin_permission
from db_sessions import session_roles_aj

from flask_restful import reqparse, abort, Resource, fields, marshal_with
from app.admodels import Action, ChildService

# class Action(db.Model):
#     __tablename__ = 'action'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     services = db.relationship('ChildService', secondary=childservice_action)
#
#     def __repr__(self):
#         return '<action %r>' % self.name

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'uri': fields.Url('api.action', absolute=True),
    'services': fields.List(fields.Nested(
        {

            'id': fields.String(),
            'name': fields.String(),

        }

    )),

}
tse_fields = {'id': fields.Integer, 'username': fields.String, 'email': fields.String, 'user_priority': fields.Integer,
              'custom_greeting': fields.FormattedString('Hey there {username}!'), 'date_created': fields.DateTime,
              'date_updated': fields.DateTime, 'links': fields.Nested(
        {'friends': fields.Url('/Users/{id}/Friends', absolute=True),
         'posts': fields.Url('Users/{id}/Posts', absolute=True),}),}

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('name', type=str)
parser.add_argument('password', type=str)
parser.add_argument('service', type=str)


class ActionResource(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        todo = session_roles_aj.query(Action).filter(Action.id == id).first()
        if not todo:
            abort(404, message="Todo {} doesn't exist".format(id))

        print(" todo:", todo, '-->File "rolo_resources.py", line 29')
        print(" todo:", todo, '-->File "rolo_resources.py", line 29')

        return todo

    def delete(self, id):
        # todo = session_roles_aj.query(Action).first()
        todo = session_roles_aj.query(Action).filter(Action.id == id).first()

        print(" todo.name:", todo.name, '-->File "actions_resources.py", line 59')
        print(" todo.name:", todo.name, '-->File "actions_resources.py", line 59')
        print(" todo.name:", todo.id, '-->File "actions_resources.py", line 59')
        print(" todo.name:", todo.id, '-->File "actions_resources.py", line 59')

        todo.services = []
        session_roles_aj.add(todo)
        session_roles_aj.commit()
        print(" commit:", '-->File "manage.py", line 63')
        session_roles_aj.delete(todo)
        session_roles_aj.commit()

        return {}, 204

    @marshal_with(user_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        user = session_roles_aj.query(Action).filter(Action.id == id).first()
        user.name = parsed_args['service']
        session_roles_aj.add(user)
        session_roles_aj.commit()
        return user, 201


class ActionListResource(Resource):
    @marshal_with(user_fields)
    # @admin_permission.require(http_exception=403)

    def get(self):
        todos = session_roles_aj.query(Action).all()
        return todos

    @marshal_with(user_fields)
    def post(self):
        # json_data = request.get_json(force=True)
        print(" json_data post :", '-->File "rolo_resources.py", line 110')
        print(" json_data post :", '-->File "rolo_resources.py", line 110')
        print(" json_data post :", '-->File "rolo_resources.py", line 110')
        print(" json_data post :", '-->File "rolo_resources.py", line 110')
        print(" json_data post :", '-->File "rolo_resources.py", line 110')
        # print(" json_data:", json_data, '-->File "rolo_resources.py", line 110')
        # print(" json_data:", json_data, '-->File "rolo_resources.py", line 110')



        parsed_args = parser.parse_args()
        input_service = parsed_args['service']
        input_name = parsed_args['name']

        tell = session_roles_aj.query(Action).filter(Action.name == input_name).first()

        if tell is not None:
            return tell

        todo = Action(name=parsed_args['name'])

        aa = ChildService(name=parsed_args['service'])
        print("  todo.services:", todo.services, '-->File "actions_resources.py", line 118')
        print("  todo.services:", todo.services, '-->File "actions_resources.py", line 118')
        print("  todo.services:", todo.services, '-->File "actions_resources.py", line 118')
        print("  todo.services:", todo.services, '-->File "actions_resources.py", line 118')
        print("  todo.services:", todo.services, '-->File "actions_resources.py", line 118')
        print("  todo.services:", todo.services, '-->File "actions_resources.py", line 118')

        todo.services.append(session_roles_aj.query(ChildService).first())
        session_roles_aj.add(todo)

        # session_roles.commit()
        try:
            session_roles_aj.commit()
        except:
            print(" rollback:", '-->File "rolo_resources.py", line 132')

            session_roles_aj.rollback()

        return todo, 201
