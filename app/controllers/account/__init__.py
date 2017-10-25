from flask import Blueprint
from flask_login import login_user, logout_user, login_required
from flask_principal import (
    AnonymousIdentity,
    Identity,
    identity_changed,
)

from app.admodels import User
from db_sessions import session_roles, session_roles_aj
from extensions import role_admin, admin_permission, user_permission, editor_permission, current_privileges, \
    super_permission
# from roles import User, Role
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

account = Blueprint('account', __name__, 'templates',
                    url_prefix='/account')


@account.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        u_name = request.form['name']
        u_password = request.form['password']
        print(" u_email:", u_name, '-->File "__init__.py", line 48')
        print(" u_password:", u_password, '-->File "__init__.py", line 48')

        usr = session_roles_aj.query(User).filter(User.username == u_name).first()

        # user = session_roles.query(User).first()
        if usr is not None:

            print(" u_password:", u_password, '-->File "__init__.py", line 66')
            print(" usr.check_password(u_password):", usr.check_password(u_password), '-->File "__init__.py", line 67')

            if usr.check_password(u_password):
                login_user(usr, True)
                user_id = usr.role.name
                if user_id:
                    print(" user_id:", user_id, '-->File "__init__.py", line 55')

                    identity = Identity(user_id)
                    identity_changed.send(current_app._get_current_object(), identity=identity)
                    return redirect(url_for('account.index'))
                else:
                    return abort(401)

    return render_template('account/login.html')


@account.route('/admin')
@admin_permission.require(http_exception=403)
def admin():
    return render_template('account/admin.html')


@account.route('/')
def index():
    return render_template('account/index.html')


@account.route('/edit')
@editor_permission.require(http_exception=403)
def editor():
    return render_template('account/editor.html')


@account.route('/about')
@login_required
def about():
    return render_template('account/about.html')


@account.route("/logout")
def logout():
    print(" session:", session, '-->File "__init__.py", line 109')

    for key in ['identity.id', 'identity.auth_type']:
        session.pop(key, None)
    # session.pop(key, None)

    identity_changed.send(
        current_app._get_current_object(), identity=AnonymousIdentity())
    flash(u'你已经注销！')
    logout_user()
    return render_template('account/logout.html')


@account.errorhandler(401)
def authentication_failed(e):
    flash('Authenticated failed.')
    return redirect(url_for('account.login'))


@account.errorhandler(403)
def authorisation_failed(e):
    flash(('Your current identity is {id}. You need special privileges to'
           ' access this page').format(id=g.identity.id))

    return render_template('account/privileges.html', priv=current_privileges())
