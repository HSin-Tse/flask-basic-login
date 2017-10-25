from flask_login import UserMixin

from extensions import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(16))
    mail = db.Column(db.String(64), unique=True, index=True)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def is_authenticated(self):
        return True

    def is_actice(self):
        return True

    def is_anonymous(self):
        return False

    def get_username(self):
        return self.username

    def __repr__(self):
        return '<User %r>' % self.username

    def login(self):
        db.login_user(self)
