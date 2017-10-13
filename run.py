from flask import (
    Flask,
)

from flask_admin import Admin
from admin_helper.adminhelper import MyView

from api.api import api_bp  # module
from extensions import principals, role_admin, role_editor, action_sign_in
from ro.views import hell  # module

from flask_principal import (
    identity_loaded,
)

from flask_login import LoginManager,login_required

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx')

principals.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
# @login_required
def hello():
    return "Hello World!"


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    needs = []

    if identity.id in ('the_only_user', 'the_only_editor', 'the_only_admin'):
        needs.append(action_sign_in)

    if identity.id in ('the_only_editor', 'the_only_admin'):
        needs.append(role_editor)

    if identity.id == 'the_only_admin':
        needs.append(role_admin)

    for n in needs:
        identity.provides.add(n)


if __name__ == '__main__':
    admin = Admin(app, name='Tse')
    admin.add_view(MyView(name='Hello'))

    app.register_blueprint(hell)
    app.register_blueprint(api_bp)

    app.run(debug=True)
