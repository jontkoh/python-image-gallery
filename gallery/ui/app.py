from flask import Flask
from flask import request
from flask import render_template
import psycopg2
import json
from . secrets import get_secret_image_gallery

connection = None

def get_secret():
    jsonString = get_secret_image_gallery()
    return json.loads(jsonString)

def get_password(secret):
    return secret['password']

def get_host(secret):
    return secret['host']

def get_username(secret):
    return secret['username']

def get_dbname(secret):
    return secret['database_name']

def connect():
    global connection
    secret = get_secret()
    connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret), password=get_password(secret))
    cursor = connection.cursor()

def execute(query):
    global connection
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.close()
    connection.close()

#function for listing users
def listUsers():
    cursor = connection.cursor() 
    cursor.execute('SELECT username, full_name FROM users;')
    username = cursor.fetchall()
    cursor.close()
    connection.close()
    return username

#function for deleting users
def deleteUser(user):
    global connection
    cursor = connection.cursor()
    pgDelete = "DELETE from users where username = '" + user + "'"
    cursor.execute(pgDelete)
    connection.commit()
    cursor.close()
    connection.close()

#function for editing users
def editUsers(user, password, fullName):
    global connection
    cursor = connection.cursor()
    pgUpdate = """Update users set password = %s where username = %s"""
    cursor.execute(pgUpdate, (password, user))

    pgUpdate = """Update users set full_name = %s where username = %s"""
    cursor.execute(pgUpdate, (fullName, user))
    connection.commit()
    cursor.close()
    connection.close()

#function for creating users
def createUser(user, password, fullName):
    global connection
    cursor = connection.cursor()
    pgInsert = """INSERT INTO users (username, password, full_name) values (%s, %s, %s)"""
    record = (user, password, fullName)
    cursor.execute(pgInsert, record)
    connection.commit()
    cursor.close()
    connection.close()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'please go to /admin'

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
