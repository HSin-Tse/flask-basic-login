from flask import (
    Flask,
)

from flask_principal import identity_loaded

from extensions import principals, action_sign_in, role_editor, role_admin, login_manager


def create_app(config_filename):
    app = Flask(__name__)
    principals.init_app(app)

    app.config.update(
        DEBUG=True,
        SECRET_KEY='secret_xxx')
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
    app.register_blueprint(hell)
    app.register_blueprint(api_bp)

    return app
