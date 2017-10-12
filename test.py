import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))  # basedir: /Users/tse/Documents/flask/stat-api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# sqlite:////Users/tse/Documents/flask/stat-api/data.sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'datatest.sqlite')

db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


# db.drop_all()
db.create_all()


admin_role = Role(name='admin')
edit_role = Role(name='edit')
see_role = Role(name='see')

user_admin = User(username='tse', role=admin_role)
user_edit = User(username='canedit', role=admin_role)
user_see = User(username='cansee', role=admin_role)

rolist = [admin_role, edit_role, see_role]





# db.session.add_all(rolist)
# db.session.commit()

print(" Role.query.all():", Role.query.all(), '-->File "test.py", line 52')
print(" User.query.all():", User.query.all(), '-->File "test.py", line 52')

print(admin_role.id)
