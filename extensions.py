from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_principal import (
    ActionNeed,
    Permission,
    Principal,
    RoleNeed)
from flask import (
    g,
)
from flask_sqlalchemy import SQLAlchemy

from db_sessions import session_roles_aj

# from roles import User

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'
login_manager.login_message = u"请登录！"

principals = Principal()

# Needs
role_admin = RoleNeed('admin')
role_editor = RoleNeed('editor')
role_super_admin = RoleNeed('superAdmin')

action_sign_in = ActionNeed('signIn')

# Permissions
super_permission = Permission(role_super_admin,action_sign_in,role_admin)

editor_permission = Permission(role_editor)
admin_permission = Permission(role_admin)

user_permission = Permission(action_sign_in)

# apps_permissions = [user_permission, editor_permission, admin_permission]
apps_needs = [role_admin, role_editor, action_sign_in]

db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()


def current_privileges():
    return (('{method} : {value}').format(method=n.method, value=n.value)
            for n in apps_needs if n in g.identity.provides)


@login_manager.user_loader
def load_user(user_id):
    from app.admodels import User
    user = session_roles_aj.query(User).filter_by(id=user_id).first()
    # usr = session_roles_aj.query(User).filter(User.username == u_name).first()

    # user =User.get_id(user_id)

    return user
