import datetime

import flask

import config
import login
import api
import views


app = flask.Flask(
    __name__, template_folder=config.TEMPLATE_FOLDER, static_folder=config.STATIC_FOLDER
)
app.secret_key = config.FLASK_SECRET_KEY
app.config["REMEMBER_COOKIE_DURATION"] = datetime.timedelta(
    days=config.REMEMBER_COOKIE_DURATION
)
app.config['UPLOAD_FOLDER'] = '/temp'

login.login_manager.init_app(app)
app.register_blueprint(api.api, url_prefix="/api/")
app.register_blueprint(views.views)
