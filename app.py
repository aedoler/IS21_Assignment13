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
        cur = g.db.execute('SELECT id, name, last_name FROM students order by last_name')
        students = [dict(id=row[0], name=row[1], last_name=row[2]) for row in cur.fetchall()]
        for item in students:
            print item

        return render_template('dashboard.html', students = students)





if __name__ == "__main__":
    app.run()
    connect_db()