#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize SQLite database
conn = sqlite3.connect('neighborhood_help.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT UNIQUE,
        role TEXT,
        skills TEXT,
        location TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        title TEXT,
        description TEXT,
        category TEXT,
        budget REAL,
        location TEXT,
        status TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        reviewer_id TEXT,
        rating INTEGER,
        comment TEXT
    )
''')
conn.commit()

# Mock user class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    cursor.execute("SELECT id, username, role FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user:
        return User(id=user[0], username=user[1], role=user[2])
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']
        skills = request.form.get('skills', '')
        location = request.form['location']
        
        user_id = str(uuid.uuid4())
        cursor.execute("INSERT INTO users (id, username, password, email, role, skills, location) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (user_id, username, password, email, role, skills, location))
        conn.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor.execute("SELECT id, username, role FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        if user:
            user_obj = User(id=user[0], username=user[1], role=user[2])
            login_user(user_obj)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'helper':
        cursor.execute("SELECT * FROM jobs WHERE status = 'open'")
        jobs = cursor.fetchall()
        return render_template('dashboard_helper.html', jobs=jobs)
    else:
        cursor.execute("SELECT * FROM jobs WHERE user_id = ?", (current_user.id,))
        jobs = cursor.fetchall()
        return render_template('dashboard_user.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
@login_required
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        budget = request.form['budget']
        location = request.form['location']
        
        job_id = str(uuid.uuid4())
        cursor.execute("INSERT INTO jobs (id, user_id, title, description, category, budget, location, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (job_id, current_user.id, title, description, category, budget, location, 'open'))
        conn.commit()
        
        flash('Job posted successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('post_job.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5017, debug=True)