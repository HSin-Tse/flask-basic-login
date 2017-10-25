# manage.py
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from app import create_app
from app.admodels import User, Role
from db_sessions import session_roles_aj
from extensions import db
from run import app

# app = create_app('config')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("r", Server())
manager.add_command('db', MigrateCommand)


@manager.command
def he():
    print('hello')


@manager.shell
def make_shell_context():
    return dict(app=app)


@manager.command
def cr_ad():
    """Creates the admin user."""
    admin_role = Role(name='aaa')
    editor_role = Role(name='admin')

    todo = User(password='aaa', username='test', mail='aaa',confirmed=True,role=admin_role)
    # session_roles_aj.add(todo)
    # db.session.add(User("ad@min.com", "admin"))
    session_roles_aj.add(todo)
    session_roles_aj.commit()


if __name__ == '__main__':
    manager.run()
