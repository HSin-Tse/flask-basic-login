from flask import url_for
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView

from flask_login import login_required, current_user
from wtforms import PasswordField

from app.admodels import User
from extensions import admin_permission


class CustomModelView(ModelView):
    """View function of Flask-Admin for Models page."""

    def is_accessible(self):
        """Setup the access permission for CustomModelView."""

        return current_user.is_authenticated and admin_permission.can()


class CustomUserModelView(ModelView):
    """View function of Flask-Admin for Models page."""

    def is_accessible(self):
        """Setup the access permission for CustomModelView."""

        return current_user.is_authenticated and admin_permission.can()


class CustomFileAdmin(FileAdmin):
    """File System admin."""

    def is_accessible(self):
        """Setup the access permission for CustomFileAdmin."""

        return current_user.is_authenticated and admin_permission.can()


class UserView(ModelView):
    form_excluded_columns = ('password')
    #  Form will now use all the other fields in the model

    # #  Add our own password form field - call it password2
    form_extra_fields = {
        'password': PasswordField('Password')
    }

    # set the form fields to use
    form_columns = (
        'username',
        'password',
        'mail',
        'confirmed',
        'role',
    )
    list_columns = (
        'id',
        'username',
        # 'password',
        'mail',
        'confirmed',
        'role',
    )
    column_searchable_list = (User.username,)

    def on_model_change(self, form, user, is_created):
        if form.password.data is not None:
            user.password = user.set_password(form.password.data)


class ChildServiceModol(ModelView):
    form_columns = (
        'id',
        'name',
        'tags',
        # 'users',
    )
    list_columns = (
        'id',
        'name',
        'tags',
        # 'users',
    )
    column_searchable_list = (User.username,)


# class ChildService(db.Model):
#     __tablename__ = 'childservice'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#
#     tags = db.relationship('Action', secondary=childservice_action, backref=db.backref('childservice'))
#
#     users = db.relationship('Role', backref='childservice', lazy='dynamic')
#
#     def __repr__(self):
#         return '<Role %r>' % self.name

# id = db.Column(db.Integer, primary_key=True)
# username = db.Column(db.String(64), unique=True, index=True)
# password = db.Column(db.String(16))
# mail = db.Column(db.String(64), unique=True, index=True)
# confirmed = db.Column(db.Boolean, nullable=False, default=False)
# role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


class MyView(BaseView):
    @expose('/')
    def index(self):
        return "aaaa"

    # def index(self):
    #     return url_for('account.index')

    @expose('/second_page')
    def second_page(self):
        return "s"
