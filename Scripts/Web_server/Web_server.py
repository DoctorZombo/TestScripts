from flask import request, Flask, render_template, abort, send_from_directory, flash, redirect, session, Response
import flask_wtf
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.utils import secure_filename
from datetime import timedelta
from pathlib import Path
from waitress import serve
import os
#C:/Users/User/Documents/GitHub/TestScripts/Scripts/output/Web_server

#C:/Users/User/Documents/GitHub/TestScripts/Scripts/output/Web_server/uploads

#C:/Users/Администратор/Desktop/Сервер/Web_server

#C:/Users/Администратор/Desktop/Сервер/Web_server/uploads

disk = Flask(__name__)
UPLOAD_FOLDER = 'C:/Users/Администратор/Desktop/Сервер/Web_server/uploads' #папка с файлами
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'} #разрешеные типы файлов
Filter_EXTENSIONS = False
disk.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
disk.config['SECRET_KEY'] = 'ваш_секретный_ключ'
disk.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///disk.db' #база данных
disk.config['SQLALCHEMY_DATABASE_OPTIONS'] = {'check_same_thread': False}
db = SQLAlchemy(disk)
disk.permanent_session_lifetime = timedelta(days=1)
max_size_mb = 100
max_size_bytes = max_size_mb * 1024**2


"""Функции и классы"""
disk.template_folder = os.path.join('C:/Users/Администратор/Desktop/Сервер/Web_server', 'templates')
server_crt = Path('C:/Users/Администратор/Desktop/Сервер/Web_server/server.crt')
server_key = Path('C:/Users/Администратор/Desktop/Сервер/Web_server/server.key')
def allowed_file(filename): #проверяет расширения файлов
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_tables(): #создает все таблицы при запуске
    db.create_all()

def profile(user):
    session['username'] = user
    session.permanent = True

def init_db():
    with disk.app_context():
        db.create_all()


def users_check():
    with disk.app_context():
        users = User.query.all()
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Passwor hash: {user.password_hash}")

def contents_check(username, path):
    contents = {
        'files': [],
        'subdirs': [],
        'current_path': Path(path)
    }
    try:
        items = Path(path).iterdir()
        for item in items:
            full_path = Path(path).joinpath(item)
            if Path(full_path).is_dir():
                contents['subdirs'].append({
                    'name': Path(item).name,
                    'path': Path(item)
                })
            else:
                contents['files'].append({
                    'name': Path(item).name,
                    'path': Path(item)
                })
        print(contents['current_path'])
    except FileNotFoundError:
        Path(disk.config['UPLOAD_FOLDER']).joinpath(username).mkdir(exist_ok=True)  # создаем папку при ее отсутствии
    print(contents)
    return contents

def total_size_check():
    username = session['username']
    total_size = sum(f.stat().st_size for f in Path('uploads').joinpath(username).rglob('**/*'))
    return total_size

class RegisterForm(flask_wtf.FlaskForm): #форма регистрации
    username = StringField('username', validators=[DataRequired()]) #ввод имя
    email = StringField('email', validators=[DataRequired(), Email()]) #ввод почты
    password = PasswordField('password', validators=[DataRequired()]) #ввод пароля
    repeat_password = PasswordField('repeat_password', validators=[DataRequired(), EqualTo('password')]) #совпадают ли пароли

class LoginForm(flask_wtf.FlaskForm):
    username = RegisterForm.username
    password = RegisterForm.password

class User(db.Model): #таблица пользователей
    id = db.Column(db.Integer, primary_key=True) #столбец id
    username = db.Column(db.String(20), unique=True, nullable=False) #столбец имен
    email = db.Column(db.String(120), unique=True, nullable=False) #столбец почт
    password_hash = db.Column(db.String(128)) #столбец хэш-паролей

    def set_password(self, password):
        self.password_hash = generate_password_hash(password) #переделывает пароль в хэш-пароль

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) #сравнивает хэш-пароль с обычным

"""Обработка запросов"""
@disk.route('/', methods=['GET', 'POST']) #загрузка и скачивание файлов
def disk_scan():
    if 'username' in session:
        username = session['username']
        total_size = total_size_check()
        contents = contents_check(username, Path(disk.config['UPLOAD_FOLDER']).joinpath(username))
        return render_template('home.html', contents=contents, total_size=f'{total_size/(1024**2):.2f}', max_size_mb=max_size_mb)
    return redirect('/login')

@disk.route('/accept/<folder_path>', methods=['POST'])
def accept(folder_path):
    if 'username' not in session:
        return redirect('/login')
    total_size = total_size_check()
    username = session['username']
    # Проверяем наличие файла в запросе
    if 'file' not in request.files:
        error = 'Файл не выбран'
    else:
        file = request.files['file']
        size = request.content_length
        message = None  # сообщение об ошибке
        error = None  # сама ошибка
        # Если файл не выбран
        if file.filename == '':
            error = 'Файл не выбран'
        # Проверяем разрешенное расширение
        elif not allowed_file(file.filename) and Filter_EXTENSIONS:
            error = 'Недопустимый тип файла'
        elif total_size + size > max_size_bytes:
            error = 'На диске нет места'
        else:
            # Безопасное имя файла
            filename = secure_filename(file.filename)
            # Сохраняем файл
            file.save(Path(folder_path).joinpath(filename))
            message = f'Файл "{filename}" успешно загружен'
            contents = contents_check(username, Path(folder_path))
    return render_template('home.html', message=message, error=error, contents=contents, total_size=f'{total_size / (1024 ** 2):.2f}', max_size_mb=max_size_mb)



"""Регистрация"""
@disk.route('/reg', methods=['GET', 'POST'])
def reg():
    if 'username' not in session:
        form = RegisterForm()  # получаем форму регистрации
        if form.validate_on_submit():  # проверяет прошли ли поля валидацию и является ли запрос POST
            existing_user = User.query.filter_by(
                username=form.username.data).first()  # проверяем существует ли имя в базе данных
            existing_email = User.query.filter_by(
                email=form.email.data).first()  # проверяем существует ли почта в базе данных
            if existing_user:
                flash('Имя уже занято')  # выводим сообщение
            elif existing_email:
                flash('Почта уже используется')  # выводим сообщение
            else:
                new_user = User(username=form.username.data, email=form.email.data)  # создаем нового пользователя
                print(new_user.set_password(form.password.data))  # генерируем хэш-пароль
                db.session.add(new_user)  # записываем пользователя в базу данных
                db.session.commit()  # сохраняем изменения
                print('Аккаунт создан')
                flash('Регистрация прошла успешно', 'success')  # выводим пользователю сообщение об успехе регистрации
                return redirect('/login')  # возвращаем страницу с авторизацией
        return render_template('reg.html', form=form)  # перезагружает страницу при ошибке
    return redirect('/')

"""Вход"""
@disk.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' not in session:
        form = LoginForm()  # получаем форму входа
        if form.validate_on_submit():
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user and existing_user.check_password(form.password.data):
                print('Пользователь вошел успешно')
                profile(request.form['username'])
                return redirect('/')
        return render_template('login.html', form=form)
    return redirect('/')

"""Выход"""
@disk.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('login')

@disk.route('/download/<file_path>') #скачивание пользователю
def download(file_path):
    if 'username' not in session:
        return redirect('/login')
    def generate():
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):  # Читаем по 8KB за раз
                yield chunk  # Отправляем чанк клиенту
    return Response(
        generate(),  # Генератор чанков
        headers={
            'Content-Disposition': f'attachment; filename={Path(file_path).name}'
        }
    )

@disk.route('/delete/<file_path>')
def delete(file_path):
    if 'username' not in session:
        return redirect('/login')
    if file_path:
        try:
            os.remove(file_path)
        except Exception as e:
            print('No file')
    contents = contents_check(session['username'], Path(file_path).parent)
    return render_template('home.html', contents=contents, total_size=f'{total_size_check()/(1024**2):.2f}', max_size_mb=max_size_mb)

@disk.route('/check/<folder_path>')
def check(folder_path):
    contents = contents_check(session['username'], folder_path)
    return render_template('home.html', contents=contents, total_size=f'{total_size_check()/(1024**2):.2f}', max_size_mb=max_size_mb)

if __name__ == '__main__': #запуск программы
    init_db()
    users_check()
    serve(disk, host='0.0.0.0', port=5000)
