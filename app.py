#!user/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, session, g, url_for, flash
import sqlite3
from contextlib import closing

DATABASE = 'hw13.db'
DEBUG = True
SECRET_KEY = 'secret_key'
USERNAME = 'admin'
PASSWORD = 'password'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def get_db():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def hello_world():

    return redirect('/login')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            return redirect('/dashboard')

    return render_template('login.html', error=error)

@app.route('/dashboard', methods = ['GET'])
def dashboard():
    if session['logged_in'] != True:
        return redirect('/login')
    else:
        cur = g.db.execute('SELECT id, name, last_name FROM students order by id')
        students = [dict(id=row[0], name=row[1], last_name=row[2]) for row in cur.fetchall()]
        cur2 = g.db.execute('SELECT id, subject, num_questions FROM quizzes order by id')
        quizzes = [dict(id=row[0], subject=row[1], num_questions=row[2]) for row in cur2.fetchall()]

        return render_template('dashboard.html', students = students, quizzes = quizzes)

@app.route('/student/add', methods = ['GET', 'POST'])
def add_student():
    if session['logged_in'] != True:
        return redirect('/login')
    if request.method == 'GET':
        return render_template('add_students.html')

    if request.method == 'POST':
        g.db.execute('INSERT INTO students (name, last_name) VALUES (?, ?),', [request.form['name'], request.form['last_name']])
        g.db.commit()

        return redirect('/dashboard')







if __name__ == "__main__":
    app.run()
    connect_db()