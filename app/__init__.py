from flask import (
    Flask,
)

from flask_principal import identity_loaded

from extensions import principals, action_sign_in, role_editor, role_admin, login_manager, db


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    principals.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

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

    from ro.views import hell  # module
    from api.api import api_bp  # module
    from app.controllers.account import account
    # app.register_blueprint(hell)
    app.register_blueprint(api_bp)
    app.register_blueprint(account)

    return app
