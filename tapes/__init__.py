from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '<f4b3a795f12ea88e7857c8f418c03ddcaaf3d60ebb6f76a3>'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c21022750:F6LxBcPUcWLidbn@csmysql.cs.cf.ac.uk:3306/c21022750_mvp_database'

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from tapes.models import User
from tapes.views import AdminView
admin = Admin(app,name="Admin Panel", template_mode="bootstrap3")
admin.add_view(AdminView(User,db.session))


# This function implements error logging which are posted to the tmp/errors.log file
#if not app.debug:
#    import logging
#    from logging.handlers import RotatingFileHandler
#    file_handler = RotatingFileHandler('tmp/errors.log', 'a', 1 * 1024 * 1024, 10)
#    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
#    app.logger.setLevel(logging.INFO)
#    file_handler.setLevel(logging.INFO)
#    app.logger.addHandler(file_handler)
#    app.logger.info('Blog errors')

from tapes import routes, models
