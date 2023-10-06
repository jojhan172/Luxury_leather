from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

from config import config

# Models
from models.ModelUser import ModelUser

# Entities
from models.entities.User import User

app = Flask(__name__)
db = MySQL(app)
    
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('auth/home1.html')

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
                return redirect(url_for('home'))
            else: 
                print("Wrong password")
                return render_template('auth/login2.html')

        else:
            print("User not found")
            return render_template('auth/login2.html')
    else:
        return render_template('auth/login2.html')



if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()