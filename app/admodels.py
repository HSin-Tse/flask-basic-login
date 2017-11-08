import datetime
from flask_login import UserMixin, login_user

from extensions import db, bcrypt

childservice_action = db.Table('childservice_action',
                               db.Column('childservice_id', db.Integer, db.ForeignKey('childservice.id')
                                         ),
                               db.Column('action_id', db.Integer, db.ForeignKey('action.id'))
                               )

childservice_role = db.Table('association',
                             db.Column('childservice_id', db.Integer, db.ForeignKey('childservice.id')),
                             db.Column('roles_id', db.Integer, db.ForeignKey('roles.id'))
                             )


class Action(db.Model):
    __tablename__ = 'action'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    services = db.relationship('ChildService', secondary=childservice_action)

    def __repr__(self):
        return '<action %r>' % self.name


class ChildService(db.Model):
    __tablename__ = 'childservice'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    roles = db.relationship("Role", secondary=childservice_role)

    actions = db.relationship('Action', secondary=childservice_action)

    def __repr__(self):
        return '<Service %r>' % self.name


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    service = db.relationship("ChildService", secondary=childservice_role)

    users = db.relationship('User', backref='role')  # 一對多  Role<==>User

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(255))
    mail = db.Column(db.String(64), unique=True, index=True)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'),default=1)  # 一對多  Role<==>User
    # create_time = db.Column(db.datetime, default=datetime.now)
    # time = db.Column(db.Date, default=db.datetime.utcnow)

    def set_password(self, password):
        """Convert the password to cryptograph via flask-bcrypt"""
        self.password = password
        return bcrypt.generate_password_hash(password)

    def check_password(self, password):
        print(" password:", password, '-->File "admodels.py", line 42')

        """Check the entry-password whether as same as user.password."""
        return bcrypt.check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_actice(self):
        return True

    def is_anonymous(self):
        return False

    def get_username(self):
        return self.username

    def login(self):
        login_user(self)

    def __repr__(self):
        return '<User %r>' % self.username
