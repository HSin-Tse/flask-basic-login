from flask_principal import (
    ActionNeed,
    AnonymousIdentity,
    Identity,
    identity_changed,
    identity_loaded,
    Permission,
    Principal,
    RoleNeed)

principals = Principal()

# Needs
role_admin = RoleNeed('admin')
role_editor = RoleNeed('editor')

action_sign_in = ActionNeed('sign in')

# Permissions
editor_permission = Permission(role_editor)
admin_permission = Permission(role_admin)

user_permission = Permission(action_sign_in)
