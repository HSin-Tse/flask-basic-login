from flask_login import LoginManager
from flask_principal import (
    ActionNeed,
    AnonymousIdentity,
    Identity,
    identity_changed,
    identity_loaded,
    Permission,
    Principal,
    RoleNeed)
from flask import (
    abort,
    flash,
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    current_app,
    url_for)

from db import session_roles
from roles import User

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = u"请登录！"

principals = Principal()

# Needs
role_admin = RoleNeed('admin')
role_editor = RoleNeed('editor')

action_sign_in = ActionNeed('sign in')
# apps_needs = [role_admin, role_editor, action_sign_in]

# Permissions
editor_permission = Permission(role_editor)
admin_permission = Permission(role_admin)

user_permission = Permission(action_sign_in)

apps_permissions = [user_permission, editor_permission, admin_permission]
apps_needs = [role_admin, role_editor, action_sign_in]


def current_privileges():
    return (('{method} : {value}').format(method=n.method, value=n.value)
            for n in apps_needs if n in g.identity.provides)


@login_manager.user_loader
def load_user(user_id):
    print(" user_id:", user_id, '-->File "extensions.py", line 57')
    print(" user_id:", user_id, '-->File "extensions.py", line 57')
    print(" user_id:", user_id, '-->File "extensions.py", line 57')
    print(" user_id:", user_id, '-->File "extensions.py", line 57')
    print(" user_id:", user_id, '-->File "extensions.py", line 57')

    user = session_roles.query(User).filter_by(id=user_id).first()

    # user = User()
    return user
    # 以上这段是新增加的============
