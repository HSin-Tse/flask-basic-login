import os

from flask import (
    Flask,
)
from flask_cors import CORS
from flask_login import current_user
from flask_principal import identity_loaded, ActionNeed, RoleNeed
# from flask_wtf import CsrfProtect

from extensions import principals, action_sign_in, role_editor, role_admin, login_manager, db, mail, bcrypt, cache


def create_app(config_filename):
    app = Flask(__name__)
    mail.init_app(app)

    CORS(app)
    app.config.from_object(config_filename)

    principals.init_app(app)
    db.init_app(app)
    # CsrfProtect(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)



    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):

        identity.user = current_user
        if current_user.is_authenticated:
            print(" current_user:", current_user, '-->File "__init__.py", line 31')
            print(" identity:", identity, '-->File "__init__.py", line 31')
            print(" current_user.role:", current_user.role, '-->File "__init__.py", line 32')
            print(" current_user.role.name:", current_user.role.name, '-->File "__init__.py", line 32')

            needs = []
            # action_sign_in = ActionNeed('sign in')

            needs.append(RoleNeed(current_user.role.name))
            # needs.append(ActionNeed(current_user.role.childservice.name))

            # if current_user.role.name in ('user', 'editor', 'admin'):
            #     needs.append(action_sign_in)
            #
            # if current_user.role.name in ('editor', 'admin'):
            #     needs.append(role_editor)
            #
            # if current_user.role.name == 'admin':
            #     needs.append(role_admin)
            # print(" needs:", needs, '-->File "__init__.py", line 33')

            for n in needs:
                identity.provides.add(n)

    from app.controllers.account import account
    from app.api import api_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(account)
    app.config.update(
        MAIL_SERVER='smtp.partner.outlook.cn',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_DEFAULT_SENDER=os.environ.get('MAIL_USERNAME'),
        MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
        MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    )
    return app
