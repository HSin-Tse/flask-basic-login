from flask import url_for
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView

from flask_login import login_required, current_user
from wtforms import PasswordField

from app.admodels import User, Role, ChildService, Action
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


class RoleModol(ModelView):
    form_columns = (
        'name',
        'users',
    )
    list_columns = (
        'name',
        'service',
        'users',
        # 'users',
    )
    column_searchable_list = (Role.name,)


class ChildServiceModol(ModelView):
    form_columns = (
        # 'id',
        'name',
        'children',
        'actions',
    )
    list_columns = (
        # 'id',
        'name',
        'children',
        'actions',
    )
    column_searchable_list = (ChildService.name,)


class ActionModol(ModelView):
    form_columns = (
        # 'id',
        'name',
        'services',
        # 'users',
    )
    list_columns = (
        # 'id',
        'name',
        'services',
        # 'users',
    )
    column_searchable_list = (Action.name,)


class MyView(BaseView):
    @expose('/')
    def index(self):
        return "aaaa"

    # def index(self):
    #     return url_for('account.index')

    @expose('/second_page')
    def second_page(self):
        return "s"
