from flask import Flask
from flask import request
from flask import render_template
import psycopg2
#from ..aws.secrets import get_secret_image_gallery
from ..data.db import *
from ..data.user import User
from ..data.postgres_user_dao import PostgresUserDAO

app = Flask(__name__)

connect()

def get_user_dao():
    return PostgresUserDAO()

@app.route('/')
def hello_world():
    return 'please go to /admin'

@app.route('/users')
def users():
    result = ""
    for user in get_user_dao().get_users():
        result += str(user)
    return result

@app.route('/admin')
def hello_admin():
    connect()
    row = listUsers()
    return render_template('admin.html', rows=row)

@app.route('/admin/createUser')
def create_user():
    return render_template('createUser.html')

@app.route('/admin/userCreated', methods=['POST'])
def user_created():
    user = request.form['username']
    password = request.form['password']
    fullName = request.form['fullName']
    connect()
    createUser(user, password, fullName)
    return render_template('userCreated.html', username=user, password=password, fullname=fullName) 

@app.route('/admin/user')
def hello_user():
    return 'Hello, user'

@app.route('/admin/user/edit')
def edit():
    return render_template('edit.html')

@app.route('/admin/user/editUser', methods=['POST'])
def edit_user():
    return render_template('editUser.html')

@app.route('/admin/user/editConfirmed', methods=['POST'])
def edit_confirmed():
    user = request.form['username']
    password = request.form['password']
    fullName = request.form['fullName']
    connect()
    editUsers(user, password, fullName)
    return render_template('editConfirmed.html', username=user,password=password, fullname=fullName)

@app.route('/admin/user/delete')
def delete_confirmation():
    return render_template('delete.html')

@app.route('/admin/user/deleteConfirmed', methods=['POST'])
def delete_confirmed():
    userToDelete = request.form['username']
    connect()
    deleteUser(userToDelete)
    return render_template('deleteConfirmed.html', user=userToDelete)
