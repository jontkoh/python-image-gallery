from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import session

import psycopg2
from ..data.db import *
from ..data.user import User
from ..data.postgres_user_dao import PostgresUserDAO
from ..aws.secrets import get_secret_flask_session

app = Flask(__name__)
app.secret_key = get_secret_flask_session()

connect()

def check_admin():
    return 'username' in session and session['username'] == 'admin'

def get_user_dao():
    return PostgresUserDAO()

@app.route('/')
def hello_world():
    return 'please go to /admin'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = get_user_dao().get_user_by_username(request.form["username"])
        if user is None or user.password != request.form["password"]:
            return redirect('/invalidLogin')
        else:
            session['username'] = request.form["username"]
            return redirect("/debugSession")
    else: 
        return render_template('login.html')

@app.route('/invalidLogin')
def invalid_login():
    return "Invalid"

@app.route('/admin')
def hello_admin():
    if not check_admin():
        return redirect('/login')
    connect()
    row = listUsers()
    return render_template('admin.html', rows=row)

@app.route('/admin/createUser')
def create_user():
    if not check_admin():
        return redirect('/login')
    return render_template('createUser.html')

@app.route('/admin/userCreated', methods=['POST'])
def user_created():
    if not check_admin():
        return redirect('/login')
    user = request.form['username']
    password = request.form['password']
    fullName = request.form['fullName']
    connect()
    createUser(user, password, fullName)
    return render_template('userCreated.html', username=user, password=password, fullname=fullName) 

@app.route('/admin/user')
def hello_user():
    if not check_admin():
        return redirect('/login')
    return 'Hello, user'

@app.route('/admin/user/edit')
def edit():
    if not check_admin():
        return redirect('/login')
    return render_template('edit.html')

@app.route('/admin/user/editUser', methods=['POST'])
def edit_user():
    if not check_admin():
        return redirect('/login')
    return render_template('editUser.html')

@app.route('/admin/user/editConfirmed', methods=['POST'])
def edit_confirmed():
    if not check_admin():
        return redirect('/login')
    user = request.form['username']
    password = request.form['password']
    fullName = request.form['fullName']
    connect()
    editUsers(user, password, fullName)
    return render_template('editConfirmed.html', username=user,password=password, fullname=fullName)

@app.route('/admin/user/delete')
def delete_confirmation():
    if not check_admin():
        return redirect('/login')
    return render_template('delete.html')

@app.route('/admin/user/deleteConfirmed', methods=['POST'])
def delete_confirmed():
    if not check_admin():
        return redirect('/login')
    userToDelete = request.form['username']
    connect()
    deleteUser(userToDelete)
    return render_template('deleteConfirmed.html', user=userToDelete)
