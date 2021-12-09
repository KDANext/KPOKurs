import flask_login
import sqla_wrapper
import config


db = sqla_wrapper.SQLAlchemy(
    f"sqlite:///{config.DATABASE_PATH}"
)


class User(db.Model, flask_login.UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    files = db.relationship("File", backref="user", lazy=True)


class File(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
