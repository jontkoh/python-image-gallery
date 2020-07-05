import psycopg2
import json
from ..aws.secrets import get_secret_image_gallery

connection = None
cursor = None

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
    global cursor
    secret = get_secret()
    connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret), password=get_password(secret))
    cursor = connection.cursor()

def execute(query):
    global connection
    global cursor
    cursor = connection.cursor()
    cursor.execute(query)



#function for listing users
def listUsers():
    global connection
    global cursor
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

    

