# manage.py
from flask_script import Manager, Server

from run import app

manager = Manager(app)
manager.add_command("run", Server(use_debugger=True))


@manager.command
def he():
    print ('hello')

if __name__ == '__main__':
    manager.run()
