import flask

import config

views = flask.Blueprint("views", __name__)

@views.route("/")
def route_index():
    return flask.render_template('index.html')
