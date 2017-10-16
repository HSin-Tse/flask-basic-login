from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView

from flask_login import login_required, current_user

from extensions import admin_permission


class CustomModelView(ModelView):
    """View function of Flask-Admin for Models page."""

    def is_accessible(self):
        """Setup the access permission for CustomModelView."""

        # callable function `User.is_authenticated()`.
        # FIXME(JMilkFan):
        #     Using function is_authenticated(),
        #     Can return the value of current_user.is_authenticated()
        #     when user was logged in.
        return current_user.is_authenticated and admin_permission.can()


class CustomFileAdmin(FileAdmin):
    """File System admin."""

    def is_accessible(self):
        """Setup the access permission for CustomFileAdmin."""

        # callable function `User.is_authenticated()`.
        return current_user.is_authenticated and admin_permission.can()


class MyView(BaseView):
    @expose('/')
    def index(self):
        return "aaaa"
