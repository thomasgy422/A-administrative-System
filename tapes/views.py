from flask_admin import model
from flask_admin.contrib.sqla import ModelView
import flask_login as login
from tapes.models import User


# This function implements the admin-view function to the website.

class AdminView(ModelView):
    def is_accessible(self):
        if login.current_user.is_authenticated:
            if login.current_user.get_id():
                user = User.query.get(login.current_user.get_id())
                return user.is_admin
        return False
