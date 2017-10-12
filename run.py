from flask import (
    abort,
    flash,
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for)

# from roles import Role, User
# from db import session_roles

from flask_admin import Admin
from admin_helper.adminhelper import MyView

from api.api import api_bp  # module
from ro.views import hell  # module

from flask_principal import (
    ActionNeed,
    AnonymousIdentity,
    Identity,
    identity_changed,
    identity_loaded,
    Permission,
    Principal,
    RoleNeed)

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx')

principals = Principal(app, skip_static=True)

# Needs
be_admin = RoleNeed('admin')
be_editor = RoleNeed('editor')

to_sign_in = ActionNeed('sign in')

# Permissions
user = Permission(to_sign_in)
user.description = "User's permissions"
editor = Permission(be_editor)
editor.description = "Editor's permissions"
admin = Permission(be_admin)
admin.description = "Admin's permissions"

apps_needs = [be_admin, be_editor, to_sign_in]
apps_permissions = [user, editor, admin]


def authenticate(email, password):
    if password == email + "user":
        return "the_only_user"
    elif password == email + "admin":
        return "the_only_admin"
    elif password == email + "editor":
        return "the_only_editor"
    else:
        return None


def current_privileges():
    return (('{method} : {value}').format(method=n.method, value=n.value)
            for n in apps_needs if n in g.identity.provides)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = authenticate(request.form['email'],
                               request.form['password'])
        print(" user_id:", user_id, '-->File "run.py", line 82')

        if user_id:
            identity = Identity(user_id)
            identity_changed.send(app, identity=identity)
            return redirect(url_for('index'))
        else:
            return abort(401)
    return render_template('login.html')


@app.route('/admin')
@admin.require(http_exception=403)
def admin():
    return render_template('admin.html')


@app.route('/edit')
@editor.require(http_exception=403)
def editor():
    return render_template('editor.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/logout")
def logout():
    for key in ['identity.id', 'identity.auth_type']:
        session.pop(key, None)
    identity_changed.send(app, identity=AnonymousIdentity())
    return render_template('logout.html')



@app.errorhandler(401)
def authentication_failed(e):
    flash('Authenticated failed.')
    return redirect(url_for('login'))


@app.errorhandler(403)
def authorisation_failed(e):
    flash(('Your current identity is {id}. You need special privileges to'
           ' access this page').format(id=g.identity.id))

    return render_template('privileges.html', priv=current_privileges())


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    needs = []

    if identity.id in ('the_only_user', 'the_only_editor', 'the_only_admin'):
        needs.append(to_sign_in)

    if identity.id in ('the_only_editor', 'the_only_admin'):
        needs.append(be_editor)

    if identity.id == 'the_only_admin':
        needs.append(be_admin)

    for n in needs:
        identity.provides.add(n)

if __name__ == '__main__':
    admin = Admin(app, name='Tse')
    admin.add_view(MyView(name='Hello'))

    app.register_blueprint(hell)
    app.register_blueprint(api_bp)

    app.run(debug=True)
