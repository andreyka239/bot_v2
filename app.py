from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Подключение к базе данных
db = SQLAlchemy(app)


# Модель данных для пользователей
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'


# Убедитесь, что создаете базу данных в контексте приложения
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Получение данных из формы
        name = request.form['name']
        email = request.form['email']

        # Создание нового пользователя и сохранение его в базу данных
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()

        # Сообщение о регистрации
        flash(f'Пользователь {name} успешно зарегистрирован!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/users')
def users():
    # Получение всех пользователей из базы данных
    users = User.query.all()
    return render_template('users.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)
