# manage.py
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from app import create_app
from app.admodels import User, Role
from db_sessions import session_roles_aj
from extensions import db, bcrypt
from run import app

# app = create_app('config')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("r", Server())
manager.add_command('db', MigrateCommand)

# bcrypt = Bcrypt()


@manager.command
def he():
    print('hello')


@manager.shell
def make_shell_context():
    return dict(app=app)


@manager.command
def cr():
    """Creates the admin user."""
    admin_role = Role(name='admin')
    editor_role = Role(name='editor')
    admi_nuser = User(password=bcrypt.generate_password_hash('admin'), username='admin', mail='admin', confirmed=True, role=admin_role)
    editer_nuser = User(password=bcrypt.generate_password_hash('editor'), username='editer', mail='editer', confirmed=True, role=editor_role)

    # session_roles_aj.add(todo)
    # db.session.add(User("ad@min.com", "admin"))
    # session_roles_aj.add(todo)
    session_roles_aj.add(admi_nuser)
    session_roles_aj.add(editer_nuser)
    session_roles_aj.commit()


@manager.command
def test():
    password = 'asd'
    secret = bcrypt.generate_password_hash(password)
    secret_2 = bcrypt.generate_password_hash(password)
    check = bcrypt.check_password_hash(secret, 'asd')
    print(" check:", check, '-->File "manage.py", line 51')

    print(" secret:", secret, '-->File "manage.py", line 48')
    print(" secret:", secret_2, '-->File "manage.py", line 48')


if __name__ == '__main__':
    manager.run()
