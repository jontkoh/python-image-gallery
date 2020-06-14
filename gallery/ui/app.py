from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, jon!'

@app.route('/admin')
def hello_admin():
    return 'Hello, admin'

@app.route('/admin/user')
def hello_user():
    return 'Hello, user'
