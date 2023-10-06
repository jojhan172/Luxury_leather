from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect

from config import config

# Models
from models.ModelUser import ModelUser

# Entities
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app) 

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)
    
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('auth/create_account.html')

@app.route('/navbar')
def navbar():
    return render_template('auth/navbar.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #print(request.form['email'])
        #print(request.form['password'])
        user = User(1, request.form['email'], request.form['password'])
        print(user)
        logged_user = ModelUser.login(db, user)
        print(logged_user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('navbar'))
            else: 
                flash("Wrong password")
                print("Wrong password")
                return render_template('auth/login.html')

        else:
            flash("User not found")
            print("User not found")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/my_account')
@login_required
def my_account():
    return render_template('auth/my_account.html')

def status_401(error):
    return redirect(url_for('login')), 404

def status_404(error):
    return "<h1>Página no encontrada</h1>"

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app) # Protección basada en csrf para evitar ataques
    app.register_error_handler(401, status_401) # Si no existe un usuario logeado se ejecutará esta función
    app.register_error_handler(404, status_404) # Si la página a la que se intenta acceder no existe, se ejecutará esta función
    app.run()
