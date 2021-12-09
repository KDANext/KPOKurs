import os

import flask
import flask_login
import sqlalchemy.exc
import werkzeug.security

import models
from models import File
import config
from FTPservice import *

api = flask.Blueprint("api", __name__)
FTPservice = FTPservice(ftp_address='127.0.0.1')

def str_field_is_true(field: str, acceptable=("1", "true")) -> bool:
    return field.strip().lower() in acceptable


@api.after_request
def set_crossdomain_headers(response):
    """This middleware provides cross-domain requests"""
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@api.route("/sign-up", methods=["POST"])
def api_signup():
    """Creates a new user

    Args:
        login
        password

    Errors:
        400: Bad Request
        403: login is not unique
    """

    try:
        login = flask.request.form["login"].strip()
        password = flask.request.form["password"].strip()
    except KeyError:
        flask.abort(400, "No login or password")

    if not login or not password:
        flask.abort(400, "Empty login or password")

    if not login.isalnum():
        flask.abort(400, "Login must contain letters and digits only")

    user = models.User(
        login=login, password=werkzeug.security.generate_password_hash(password)
    )
    models.db.s.add(user)
    FTPservice.create_user_directory(user.login)

    try:
        models.db.s.commit()
    except sqlalchemy.exc.IntegrityError:
        flask.abort(403, "Login is not unique")

    flask_login.login_user(user, remember=False)

    return "OK"


@api.route("/sign-in", methods=["POST"])
def api_singin():
    """Log in user

    Args:
        login
        password
        remember

    Errors:
        400: Bad Request
        403: Wrong password
        404: User not found
    """

    try:
        login = flask.request.form["login"].strip()
        password = flask.request.form["password"].strip()
        remember = str_field_is_true(flask.request.form["remember"])
    except KeyError:
        flask.abort(400, "No login or password")

    try:
        user = models.User.query.filter(models.User.login == login).one()
    except sqlalchemy.exc.NoResultFound:
        flask.abort(404, "User not found")

    if werkzeug.security.check_password_hash(user.password, password):
        flask_login.login_user(user, remember)
    else:
        flask.abort(403, "Wrong password")
    return "OK"


@api.route("/sign-out")
@flask_login.login_required
def api_signout():
    flask_login.logout_user()
    return "OK"


@api.route("/upload-file", methods=["POST"])
@flask_login.login_required
def api_upload_file():
    """Log in user
        Args:
            file
        Errors:
        """
    #Получаем файл
    file = flask.request.files['file']
    #Сохраняем оригинальное имя для загрузки на сервер
    temp_name_file = file.filename
    #Времено сохраняем файл в апи
    file.save(os.path.join(config.UPLOAD_FOLDER, file.filename))
    #Берем данные пользователя для дальнейшей обработки
    user = flask_login.current_user
    #Создаем запись о файле в базе данных
    file_model = File(title=file.filename, user_id=user.id)
    #Записываем в базу данных
    models.db.s.add(file_model)
    #Сохраняем базу данных
    models.db.s.commit()
    #Сохраняем файл на фтп
    FTPservice.upload_file(file_name=str(file_model.id), user_directory=user.login,
                           file_path=config.UPLOAD_FOLDER + '\\' + temp_name_file)
    os.remove(config.UPLOAD_FOLDER + '\\' + temp_name_file)
    return "OK"

@api.route("/read-file", methods=["POST"])
@flask_login.login_required
def api_read_file():
    #Считываем все файлы с базы данных принадлежащие пользователю и генерируем ссылки для этих фалов на скачивание и удаленин
    for i in models.db.s.all(models.File).filter(models.File.user_id == flask_login.current_user.id):
        print(i.title)
    return "ОК"
    
#Еще остались методы которые Скачать, Удалить, Обновить
#Поправить метод с заходом 
#Дописать метод прочитывания файлов если человек админ он может читать все файлы и удалять поговорить насчет фильтра
#
#Скачать файл пост или гет?
#Считываем ид файла
#Получаем файл с фтп сервера
#Возвращаем фалу оригинальное название
#Отдавем пользователю файл для скачивания
#
#Удалить файл скорее всего гет запрос
#Считываем ид файла
#Удалям файл из базы
#Говорим фтп удалить файл с нужным id
#
#Обновить файл пусть будет пост 
#Считываем ид файла
#Удаляем его из базы и фтп   
    
