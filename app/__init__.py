from flask import (
    Flask,
    Blueprint,
    flash,
    render_template,

)

# class MyResponse(Response):
#     default_mimetype = 'application/xml'


# http://flask.pocoo.org/docs/0.10/patterns/appfactories/
from flask_login import LoginManager
from flask_principal import identity_loaded

from extensions import principals, action_sign_in, role_editor, role_admin


def create_app(config_filename):
    app = Flask(__name__)
    # app.response_class = MyResponse
    principals.init_app(app)

    app.config.update(
        DEBUG=True,
        SECRET_KEY='secret_xxx')


    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        print(" identity:", identity, '-->File "__init__.py", line 35')
        print(" identity:", identity, '-->File "__init__.py", line 35')
        print(" identity:", identity, '-->File "__init__.py", line 35')

        needs = []
        if identity.id in ('the_only_user', 'the_only_editor', 'the_only_admin'):
            needs.append(action_sign_in)

        if identity.id in ('the_only_editor', 'the_only_admin'):
            needs.append(role_editor)

        if identity.id == 'the_only_admin':
            needs.append(role_admin)

        for n in needs:
            print(" needs:", needs, '-->File "__init__.py", line 51')

            identity.provides.add(n)

            # return "logout page"
    from ro.views import hell  # module
    from api.api import api_bp  # module
    app.register_blueprint(hell)
    app.register_blueprint(api_bp)

    return app
