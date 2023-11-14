from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect

import mysql.connector

import uuid # use uuid.uuid4() to generate a random id like -> print(uuid.uuid4())

from config import config

# Models
from models.ModelUser import ModelUser
from models.Product import Product

# Entities
from models.entities.User import Client, Seller

app = Flask(__name__)

csrf = CSRFProtect() # CSRF protection to avoid attacks

# Conection to the SQL server 
db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '123456',
    database = 'luxury_leather' 
)

# Our way to mantain a user logged, LoginManger allows lots of things but we use just one, user_loader
login_manager_app = LoginManager(app) 

def takeProducts() -> list:
    cursor = db.cursor()
    sql = "SELECT * FROM `products` LIMIT 2"
    cursor.execute(sql)
    row = list(cursor.fetchall())
    return row

def takeProductsWithLimit(limit: int) -> list:
    cursor = db.cursor()
    sql = "SELECT * FROM `products` LIMIT {}".format(limit)
    cursor.execute(sql)
    row = list(cursor.fetchall())
    return row

def takeProductsBySeller(sellerId:str) -> list:
    cursor = db.cursor() 
    sql = "SELECT * FROM `products` WHERE `sellerId` LIKE '{}'".format(sellerId)
    cursor.execute(sql)
    row = list(cursor.fetchall())
    return row

def takeProductsById(productId: str)-> list:
    cursor = db.cursor() 
    sql = "SELECT * FROM `products` WHERE `id` LIKE '{}'".format(productId)
    cursor.execute(sql)
    row = list(cursor.fetchall())
    return row

def editProduct(productId:str) -> list:
    cursor = db.cursor()
    sql= ""
    cursor.execute(sql)
    db.commit()
    return flash("El producto se edito correctamente")

def takeSellerById(sellerId: str) -> list:
    cursor  = db.cursor()
    sql = "SELECT * FROM `seller_users` WHERE `id` Like '{}'".format(sellerId)
    cursor.execute(sql)
    row = list(cursor.fetchall())
    return row

@login_manager_app.user_loader # this will allow us to mantain our user logged
def load_user(id):
    return ModelUser.get_by_id_client(db, id)

# --------------- VIEWS ----------------------

@app.route('/', methods = ['GET', 'POST'])
def index():
    return redirect(url_for('login_user_select'))

@app.route('/home', methods = ['GET', 'POST'])
def home():
    return render_template('auth/home.html', funcion=takeProducts)

@app.route('/navbar', methods = ['GET', 'POST'])
def navbar():
    return render_template('auth/navbar.html')

@app.route('/register_user_select', methods = ['GET', 'POST'])
def register_user_select():
    return render_template('auth/register__user_select.html')

@app.route('/create_account_client', methods=['GET', 'POST'])
def client_register():
    uniqueId = str(uuid.uuid4()) # Output Example -> 4f9364b3-d4b0-4012-aab2-9b4db7b17e5c
    uniqueIdProcessed = uniqueId.replace("-", "")  # we delete the "-" from the uuid because it creates conflicts with the D.B.

    if request.method == 'POST':
        newUser = Client(uniqueIdProcessed, request.form['email'], request.form['password'], request.form['fullname'], request.form['username'])
        sql = "SELECT * FROM `client_users` WHERE `email` = '{}'".format(newUser.email) # We send de SQL query from here to avoid repeating code in ModelUser
        verifier = ModelUser.VerifyRegister(db, sql) # With this we verify if the user already exist in the data base -> returns true if the user already exist
        
        if verifier == True:
            flash("Este correo ya está en uso")
            return render_template('auth/create_account_client.html')
        else: 
            sql = "INSERT INTO `client_users`(`id`, `email`, `username`, `fullname`, `password`, `postal_code`, `adress`, `city`, `phone`, `userType`) VALUES ('{uniqueId}','{email}', '{username}', '{fullname}','{password}','', '', '', '', '{userType}');".format(uniqueId = uniqueIdProcessed, email=newUser.email, username = newUser.username, fullname=newUser.fullname, password=newUser.password, userType = "client")
            
            ModelUser.addToDataBase(db, sql)
            flash("Usuario registrado correctamente.")
            return render_template('auth/create_account_client.html')
    else:
        return render_template('auth/create_account_client.html')
    
@app.route('/create_account_seller', methods=['GET', 'POST'])
def seller_register(): # -> here we do the same as for the client function
    uniqueId = str(uuid.uuid4())
    uniqueIdProcessed = uniqueId.replace("-", "") 

    if request.method == 'POST':
        newUser = Seller(uniqueIdProcessed, request.form['email'], request.form['password'], request.form['ceoName'], request.form['company'])
        sql = "SELECT * FROM `seller_users` WHERE `email` = '{}'".format(newUser.email) 
        verifier = ModelUser.VerifyRegister(db, sql) 
        
        if verifier == True:
            flash("Este correo ya está en uso")
            return render_template('auth/create_account_seller.html')
        else: 
            sql = "INSERT INTO `seller_users`(`id`, `email`, `password`, `ceoName`, `companyName`, userType) VALUES ('{uniqueId}','{email}','{password}','{ceoName}','{companyName}', '{userType}');".format(uniqueId = uniqueIdProcessed, email=newUser.email, password=newUser.password, ceoName=newUser.ceoName, companyName = newUser.companyName, userType = "seller")
            
            ModelUser.addToDataBase(db, sql)
            flash("Usuario registrado correctamente.")
            return render_template('auth/create_account_seller.html')
    else:
        return render_template('auth/create_account_seller.html')

@app.route('/login_user_select', methods = ['GET', 'POST'])
def login_user_select():
    return render_template('auth/login_user_select.html')

@app.route('/client_login', methods=['GET', 'POST'])
def client_login():
    userType = "client"

    if request.method == 'POST':
        user = Client(0, request.form['email'], request.form['password'])
        sql = "SELECT id, email, password, fullname, username, postal_code, adress, city, phone, userType FROM client_users WHERE email = '{}'".format(user.email)
        logged_user = ModelUser.login(db, user, sql, userType) # if the user exist return an object
        if logged_user != None:  # so if it's different from none we can check the password
            if logged_user.password:
                login_user(logged_user) # and we log in our use and finally our user_loader save it automaticly
                return redirect(url_for('home'))
            else: 
                flash("Wrong password")
                return render_template('auth/client_login.html')
        else:
            flash("User not found")
            return render_template('auth/client_login.html')
    else:
        return render_template('auth/client_login.html')
    
@app.route('/seller_login', methods = ['GET', 'POST'])
def seller_login():
    userType = "seller"
    if request.method == 'POST':
        user = Seller(0, request.form['email'], request.form['password'])
        sql = "SELECT id, email, password, ceoName, companyName, userType FROM seller_users WHERE email = '{}'".format(user.email)
        logged_user = ModelUser.login(db, user, sql, userType)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else: 
                flash("Wrong password")
                return render_template('auth/seller_login.html')
        else:
            flash("User not found")
            return render_template('auth/seller_login.html')
    else:
        return render_template('auth/seller_login.html')

@app.route('/my_products', methods = ['GET', 'POST'])
@login_required
def my_products():
    if request.method == 'POST':
        return render_template('auth/my_products.html', TakeProducts=takeProductsBySeller)
    else:
        return render_template('auth/my_products.html', TakeProducts=takeProductsBySeller)

@app.route('/add_new_product', methods=['GET','POST'])
def add_new_product():
    if request.method == 'POST':
        productId = uuid.uuid4()
        product = Product(productId, request.form['productName'], request.form['price'], request.form['userId'], request.form['imgURL']  )
        product.addToDb(db)
        flash("Producto agregado correctamente")
        return render_template('auth/add_new_product.html')
    else:
        return render_template('auth/add_new_product.html') 

@app.route('/view_product/<productId>/', methods=['GET','POST'])
def view_my_product(productId):
    return render_template('auth/view_product.html', productId=productId, takeProductById=takeProductsById(productId), takeSellerById=takeSellerById, takeProductsWithLimit=takeProductsWithLimit) # , ,editProduct = editProduct()

@app.route('/my_account', methods = ['GET', 'POST'])
@login_required
def my_account():
    return render_template('auth/my_account.html')

@app.route('/my_account_edit', methods = ['GET', 'POST'])
def my_account_edit():
    return render_template('auth/my_account_edit.html')

@app.route('/edit_product/<productId>')
def edit_Product(productId):
    # La idea aqui es que el programa reciba el product ID desde la pagina web y con eso
    # porderlo sacar de la base de datos para denrerizarlo
    return render_template('auth/edit_product.html', takeProductById = takeProductsById(productId))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_user_select'))

# --------------- END VIEWS ----------------------

def status_401(error):
    return redirect(url_for('client_login')), 404

def status_404(error):
    return "<h1>Página no encontrada</h1>"

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app) # CSRF protection
    app.register_error_handler(401, status_401) # If there is not an logged user this error shows up
    app.register_error_handler(404, status_404) # If the page doesn't exist this error shows up
    app.run()
