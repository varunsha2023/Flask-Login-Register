from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydata']
users = db['customers']

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = users.find_one({'username': username})
        if existing_user:
            return 'Username already exists!'
        user_id = users.insert_one({'username': username, 'password': password}).inserted_id
        session['user_id'] = str(user_id)
        return redirect(url_for('profile'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.find_one({'username': username, 'password': password})
        if user:
            session['user_id'] = str(user['_id'])
            return redirect(url_for('profile'))
        return 'Invalid username or password. Please try again.'
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        user_id = session['user_id']
        user = users.find_one({'_id': ObjectId(user_id)})
        return f'Welcome, {user["username"]}! Your user ID is {user_id}.'
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
