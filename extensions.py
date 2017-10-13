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

print(" apps_permissions:", apps_permissions[0], '-->File "extensions.py", line 27')


def current_privileges():
    return (('{method} : {value}').format(method=n.method, value=n.value)
            for n in apps_needs if n in g.identity.provides)
