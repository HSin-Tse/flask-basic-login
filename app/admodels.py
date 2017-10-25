from uuid import uuid4

from flask_login import UserMixin, login_user

from extensions import db, bcrypt


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
    password = db.Column(db.String(255))
    mail = db.Column(db.String(64), unique=True, index=True)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # def __init__(self):
    #     self.id = str(uuid4())
    # self.confirmed = confirmed


    # Setup the default-role for user.
    # default = Role.query.filter_by(name="default").one()
    # self.roles.append(default)

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
