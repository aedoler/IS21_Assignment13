#!user/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, session, g, url_for, flash
import sqlite3

DATABASE = 'hw13.db'
DEBUG = True
SECRET_KEY = 'secret_key'
USERNAME = 'admin'
PASSWORD = 'password'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.route('/')
def hello_world():

    return redirect('/login')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.form['username'] != app.config['USERNAME']:
        error = 'Invalid username'
        session['logged_in'] = True
        return redirect('/dashboard')
    elif request.form['password'] != app.config['PASSWORD']:
        error = 'Invalid password'

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
 return 'Dashboard'





if __name__ == "__main__":
    app.run()
    connect_db()