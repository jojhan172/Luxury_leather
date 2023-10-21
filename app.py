from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect

import mysql.connector

from config import config

# Models
from models.ModelUser import ModelUser

# Entities
from models.entities.User import Client, Seller

app = Flask(__name__)

csrf = CSRFProtect()
db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '123456',
    database = 'luxury_leather' 
)
login_manager_app = LoginManager(app) 

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)
    
@app.route('/')
def index():
    return redirect(url_for('client_login'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/create_account_client', methods=['GET', 'POST'])
def client_register():
    if request.method == 'POST':
        newUser = Client(0, request.form['email'], request.form['password'], request.form['fullname'], request.form['username'])
        sql = "SELECT * FROM `client_users` WHERE `email` = '{}'".format(newUser.email) # se pasa el query sql desde aqui para no tener que repetir codigo en ModelUser
        verifier = ModelUser.VerifyRegister(db, sql) # Verifica si el usuario ya esta en base de datos
        
        if verifier == True:
            flash("Este correo ya está en uso")
            return render_template('auth/create_account_client.html')
        else: 
            sql = "INSERT INTO `client_users`(`id`, `email`, `username`, `fullname`, `password`, `postal_code`, `adress`, `city`, `phone`) VALUES (Null,'{email}', '{username}', '{fullname}','{password}','', '', '', '');".format(email=newUser.email, username = newUser.username, fullname=newUser.fullname, password=newUser.password)
            ModelUser.addToDataBase(db, sql)
            flash("Usuario registrado correctamente.")
            return render_template('auth/create_account_client.html')
    else:
        return render_template('auth/create_account_client.html')
    
@app.route('/create_account_seller', methods=['GET', 'POST'])
def seller_register():
    if request.method == 'POST':
        newUser = Seller(0, request.form['email'], request.form['password'], request.form['ceoName'], request.form['company'])
        sql = "SELECT * FROM `seller_users` WHERE `email` = '{}'".format(newUser.email) # se pasa el query sql desde aqui para no tener que repetir codigo en ModelUser
        verifier = ModelUser.VerifyRegister(db, sql) # Verifica si el usuario ya esta en base de datos
        
        if verifier == True:
            flash("Este correo ya está en uso")
            return render_template('auth/create_account_seller.html')
        else: 
            sql = "INSERT INTO `seller_users`(`id`, `email`, `password`, `ceoName`, `companyName`) VALUES (Null,'{email}','{password}','{ceoName}','{companyName}'); ".format(email=newUser.email, password=newUser.password, ceoName=newUser.ceoName, companyName = newUser.companyName)
            ModelUser.addToDataBase(db, sql)
            flash("Usuario registrado correctamente.")
            return render_template('auth/create_account_seller.html')
    else:
        return render_template('auth/create_account_seller.html')

@app.route('/navbar')
def navbar():
    return render_template('auth/navbar.html')

@app.route('/user_select')
def user_select():
    return render_template('auth/login_select.html')

@app.route('/client_login', methods=['GET', 'POST'])
def client_login():
    if request.method == 'POST':
        #print(request.form['email'])
        #print(request.form['password'])
        user = Client(0, request.form['email'], request.form['password'])
        logged_user = ModelUser.client_login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('navbar'))
            else: 
                flash("Wrong password")
                return render_template('auth/client_login.html')
        else:
            flash("User not found")
            return render_template('auth/client_login.html')
    else:
        return render_template('auth/client_login.html')
    


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('client_login'))

@app.route('/my_account')
@login_required
def my_account():
    return render_template('auth/my_account.html')

def status_401(error):
    return redirect(url_for('client_login')), 404

def status_404(error):
    return "<h1>Página no encontrada</h1>"

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app) # Protección basada en csrf para evitar ataques
    app.register_error_handler(401, status_401) # Si no existe un usuario logeado se ejecutará esta función
    app.register_error_handler(404, status_404) # Si la página a la que se intenta acceder no existe, se ejecutará esta función
    app.run()
