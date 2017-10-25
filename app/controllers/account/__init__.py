from flask import Blueprint
from flask_login import login_user, logout_user, login_required
from flask_principal import (
    AnonymousIdentity,
    Identity,
    identity_changed,
)

from app.admodels import User
from db_sessions import session_roles, session_roles_aj
from extensions import role_admin, admin_permission, user_permission, editor_permission, current_privileges
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


def authenticate(email, password):
    if password == email + "user":
        return "the_only_user"
    elif password == email + "admin":
        return "the_only_admin"
    elif password == email + "editor":
        return "the_only_editor"
    else:
        return None


@account.route('/')
def index():
    return render_template('account/index.html')


@account.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        u_email = request.form['email']
        u_password = request.form['password']
        print(" u_email:", u_email, '-->File "__init__.py", line 48')
        print(" u_password:", u_password, '-->File "__init__.py", line 48')
        
        usr = session_roles_aj.query(User).filter(User.username == u_email).first()

        # user = session_roles.query(User).first()
        if usr is not None:
            # print(" usr:", usr, '-->File "__init__.py", line 52')
            # print(" usr.role:", usr.role.name, '-->File "__init__.py", line 56')
            # print(" usr.role:", usr.role.name, '-->File "__init__.py", line 56')
            # print(" usr.role:", usr.role, '-->File "__init__.py", line 56')
            # print(" usr.role:", usr.role, '-->File "__init__.py", line 56')
            #
            # print(" usr.password == u_password:", usr.password == u_password, '-->File "__init__.py", line 56')
            # print(" usr.password:", usr.password, '-->File "__init__.py", line 57')
            # print(" u_password:", u_password, '-->File "__init__.py", line 58')
            print(" u_password:", u_password, '-->File "__init__.py", line 66')
            print(" usr.check_password(u_password):", usr.check_password(u_password), '-->File "__init__.py", line 67')
            
            if usr.check_password(u_password):
            # if usr.password == u_password:
                login_user(usr, True)
                # user_id = "the_only_admin"
                user_id = usr.role.name
                if user_id:
                    print(" user_id:", user_id, '-->File "__init__.py", line 55')

                    identity = Identity(user_id)
                    identity_changed.send(current_app._get_current_object(), identity=identity)
                    return redirect(url_for('account.index'))
                else:
                    return abort(401)


            # login_user(usr, True)

            # user_id = authenticate(request.form['email'],
            #                        request.form['password'])
            # print(" user_id:", user_id, '-->File "run.py", line 82')
            # print(" user_id:", user_id, '-->File "__init__.py", line 65')
            # print(" user_id:", user_id, '-->File "__init__.py", line 65')
            # print(" user_id:", user_id, '-->File "__init__.py", line 65')
            # print(" user_id:", user_id, '-->File "__init__.py", line 65')

    return render_template('account/login.html')


@account.route('/admin')
@admin_permission.require(http_exception=403)
def admin():
    return render_template('account/admin.html')


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
    for key in ['identity.id', 'identity.auth_type']:
        session.pop(key, None)

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
