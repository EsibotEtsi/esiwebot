from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Modelo de Usuario
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

# Cargar usuario para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ruta de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta de registro (sign in)
@app.route('/sign_in', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        # Verificar si el usuario ya existe
        user = User.query.filter_by(email=email).first()
        if user:
            flash('El correo ya está registrado.')
            return redirect(url_for('signin'))

        # Crear un nuevo usuario
        new_user = User(
            email=email,
            name=name,
            password=generate_password_hash(password, method='sha256')
        )

        # Guardar el usuario en la base de datos
        db.session.add(new_user)
        db.session.commit()

        flash('Registro exitoso. Por favor, inicia sesión.')
        return redirect(url_for('login'))

    return render_template('sign_in.html')

# Ruta de inicio de sesión (login)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Buscar al usuario en la base de datos
        user = User.query.filter_by(email=email).first()

        # Verificar si el usuario existe y la contraseña es correcta
        if not user or not check_password_hash(user.password, password):
            flash('Correo o contraseña incorrectos.')
            return redirect(url_for('login'))

        # Iniciar sesión
        login_user(user)
        return redirect(url_for('index'))

    return render_template('login.html')

# Ruta de cierre de sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Ruta de galería
@app.route('/galeria')
def galeria():
    return render_template('galeria.html')

# Ruta de programación
@app.route('/programacion')
def programacion():
    return render_template('programacion.html')

# Crear la base de datos y ejecutar la aplicación
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
