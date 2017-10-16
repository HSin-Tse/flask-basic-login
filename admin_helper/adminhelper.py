from flask import Blueprint
from flask_admin import Admin, BaseView, expose, AdminIndexView


class MyView(BaseView):
    @expose('/')
    def index(self):
        return "aaaa"

# admin = Admin(admin_helper, name='My App')
# admin.add_view(MyView(name='Hello'))
