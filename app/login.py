import flask_login
import models


login_manager = flask_login.LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return models.db.s.query(models.User).get(int(user_id))
