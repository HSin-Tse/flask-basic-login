from flask import request

from extensions import user_permission, admin_permission
from db_sessions import session_roles_aj

from flask_restful import reqparse, abort, Resource, fields, marshal_with
from app.admodels import ChildService

# class ChildService(db.Model):
#     __tablename__ = 'childservice'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     children = db.relationship("Role", secondary=childservice_role)
#
#     actions = db.relationship('Action', secondary=childservice_action, backref=db.backref('childservice'))
#
#     def __repr__(self):
#         return '<Service %r>' % self.name

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'uri': fields.Url('api.service', absolute=True),
    'children': fields.List(fields.Nested(
        {

            'id': fields.String(),
            'name': fields.String(),

        }

    )),
    'actions': fields.List(fields.Nested(
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
parser.add_argument('password', type=str)


class ServiceResource(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        todo = session_roles_aj.query(ChildService).filter(ChildService.id == id).first()
        if not todo:
            abort(404, message="Todo {} doesn't exist".format(id))

        print(" todo:", todo, '-->File "rolo_resources.py", line 29')
        print(" todo:", todo, '-->File "rolo_resources.py", line 29')
        print(" todo:", todo, '-->File "rolo_resources.py", line 29')
        print(" todo:", todo, '-->File "rolo_resources.py", line 29')
        print(" todo:", todo, '-->File "rolo_resources.py", line 29')
        print(" todo:", todo, '-->File "rolo_resources.py", line 29')

        return todo

    # @user_permission.require(http_exception=403)
    def delete(self, id):
        todo = session_roles_aj.query(ChildService).filter(ChildService.id == id).first()
        if not todo:
            abort(404, message="Todo {} doesn't exist".format(id))
        session_roles_aj.delete(todo)
        session_roles_aj.commit()
        return {}, 204

    @marshal_with(user_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        user = session_roles_aj.query(ChildService).filter(ChildService.id == id).first()
        user.task = parsed_args['task']
        session_roles_aj.add(user)
        session_roles_aj.commit()
        return user, 201


class ServiceListResource(Resource):
    @marshal_with(user_fields)
    # @admin_permission.require(http_exception=403)

    def get(self):
        todos = session_roles_aj.query(ChildService).all()
        return todos

    @marshal_with(user_fields)
    def post(self):
        # json_data = request.get_json(force=True)
        # print(" json_data:", json_data, '-->File "rolo_resources.py", line 110')
        # print(" json_data:", json_data, '-->File "rolo_resources.py", line 110')
        # print(" json_data:", json_data, '-->File "rolo_resources.py", line 110')



        parsed_args = parser.parse_args()
        input_username = parsed_args['username']
        print(" input_username:", input_username, '-->File "rolo_resources.py", line 63')
        print(" input_username:", input_username, '-->File "rolo_resources.py", line 63')

        tell = session_roles_aj.query(ChildService).filter(ChildService.username == input_username).first()
        if tell is not None:
            return tell

        todo = ChildService(password=parsed_args['password'], username=parsed_args['username'])
        session_roles_aj.add(todo)

        # session_roles.commit()
        try:
            session_roles_aj.commit()
        except:
            print(" rollback:", '-->File "rolo_resources.py", line 132')

            session_roles_aj.rollback()

        return todo, 201
