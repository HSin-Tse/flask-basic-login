from flask import Blueprint
from flask_principal import (
    AnonymousIdentity,
    Identity,
    identity_changed,
)
from db import session_roles
# from extensions import role_admin
from extensions import role_admin, admin_permission, user_permission, editor_permission, current_privileges
from roles import User, Role
from flask import (
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    current_app,
    url_for)

hell = Blueprint('hell', __name__, 'templates', url_prefix='/principal')


@hell.route("/hello")
@admin_permission.require(http_exception=403)
def hello():
    return "Hello World!"


@hell.route('/test2')
def ssss():
    return render_template('testnot.html')
    # return 'ss'


# test
@hell.route('/test1')
def home():
    return render_template('test.html', roles=session_roles.query(Role).all(), users=session_roles.query(User).all(),
                           tse=session_roles.query(User).filter_by(username='tse').all()[0].role.name == 'admin')


def authenticate(email, password):
    if password == email + "user":
        return "the_only_user"
    elif password == email + "admin":
        return "the_only_admin"
    elif password == email + "editor":
        return "the_only_editor"
    else:
        return None


@hell.route('/')
def index():
    return render_template('index.html')


@hell.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        usr = session_roles.query(User).filter(User.username == request.form['email']).first()
        if usr is not None:
            print(" usr.username:", usr.username, '-->File "views.py", line 66')
            print(" usr.password:", usr.password, '-->File "views.py", line 66')

        user_id = authenticate(request.form['email'],
                               request.form['password'])
        print(" user_id:", user_id, '-->File "run.py", line 82')

        if user_id:
            identity = Identity(user_id)
            identity_changed.send(current_app._get_current_object(), identity=identity)
            return redirect(url_for('hell.index'))
        else:
            return abort(401)
    return render_template('login.html')


@hell.route('/admin')
@admin_permission.require(http_exception=403)
def admin():
    return render_template('admin.html')


@hell.route('/edit')
@editor_permission.require(http_exception=403)
def editor():
    return render_template('editor.html')


@hell.route('/about')
def about():
    return render_template('about.html')


@hell.route("/logout")
def logout():
    for key in ['identity.id', 'identity.auth_type']:
        session.pop(key, None)
    identity_changed.send(
        current_app._get_current_object(), identity=AnonymousIdentity())
    return render_template('logout.html')


@hell.errorhandler(401)
def authentication_failed(e):
    flash('Authenticated failed.')
    return redirect(url_for('hell.login'))


@hell.errorhandler(403)
def authorisation_failed(e):
    flash(('Your current identity is {id}. You need special privileges to'
           ' access this page').format(id=g.identity.id))

    return render_template('privileges.html', priv=current_privileges())
