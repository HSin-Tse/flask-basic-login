from flask import (
    Flask,
)
from flask_cors import CORS
from flask_principal import identity_loaded

from extensions import principals, action_sign_in, role_editor, role_admin, login_manager, db


def create_app(config_filename):

    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_filename)

    principals.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):

        needs = []
        print(" identity.id:", identity.id, '-->File "__init__.py", line 22')

        if identity.id in ('user', 'editor', 'admin'):
            needs.append(action_sign_in)

        if identity.id in ('editor', 'admin'):
            needs.append(role_editor)

        if identity.id == 'admin':
            needs.append(role_admin)
        print(" needs:", needs, '-->File "__init__.py", line 33')

        for n in needs:
            identity.provides.add(n)

    from app.controllers.account import account
    from app.api import api_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(account)

    return app
