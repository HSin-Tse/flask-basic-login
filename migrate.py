from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from db import session_roles
from run import app

migrate = Migrate(app, session_roles)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
