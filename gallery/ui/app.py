from flask import Flask
import psycopg2
import json
from gallery.tools.db import *



app = Flask(__name__)

@app.route('/')
def hello_world():
    return listUsers()

@app.route('/admin')
def hello_admin():
    return 'Hello, admin'

@app.route('/admin/user')
def hello_user():
    return 'Hello, user'
