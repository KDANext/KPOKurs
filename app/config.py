import os
import dotenv


dotenv.load_dotenv()
DATABASE_PATH = os.path.abspath("db.sqlite3")
TEMPLATE_FOLDER = os.path.abspath("templates")
STATIC_FOLDER = os.path.abspath("static")
REMEMBER_COOKIE_DURATION = 365  # days
FLASK_SECRET_KEY = os.environ["FLASK_SECRET_KEY"]
UPLOAD_FOLDER = 'C:\\Users\\Admin\\PycharmProjects\\pythonProject1\\temp\\'
