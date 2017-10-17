# manage.py
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from db import session_roles
from run import app

manager = Manager(app)
migrate = Migrate(app, session_roles)

manager.add_command("r", Server())
manager.add_command('db', MigrateCommand)


@manager.command
def he():
    print('hello')


if __name__ == '__main__':
    manager.run()
