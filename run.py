from roles import Role, User
from db import session_roles
from flask import (Flask,
                   render_template)
from flask_admin import Admin

from admin_helper.adminhelper import MyView
from api.api import api_bp  # module
from ro.views import hell  # module

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('test.html', roles=session_roles.query(Role).all(), users=session_roles.query(User).all(),
                           tse=session_roles.query(User).filter_by(username='tse').all()[0].role.name == 'admin')


if __name__ == '__main__':
    admin = Admin(app, name='Tse')
    admin.add_view(MyView(name='Hello'))

    app.register_blueprint(hell)
    app.register_blueprint(api_bp)

    app.run(debug=True)
