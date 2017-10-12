from flask import (Flask,
                   render_template)
from flask_admin import Admin

from admin_helper.adminhelper import MyView
from api.api import api_bp  # module
from ro.views import hell  # module

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('test.html', name='a')




if __name__ == '__main__':
    admin = Admin(app, name='Tse')
    admin.add_view(MyView(name='Hello'))

    app.register_blueprint(hell)
    app.register_blueprint(api_bp)

    app.run(debug=True)
