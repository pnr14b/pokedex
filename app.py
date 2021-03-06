from flask import Flask, render_template, redirect, \
    url_for, request, session, flash
from functools import wraps
import models as dbHandler

app = Flask(__name__)

app.secret_key = 'my precious'

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            #flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@login_required
def home():
    if request.method=='POST':
        pname = request.form['pname']
        dbHandler.addPokemon(pname)
        flash("Pokemon added")

        return redirect(url_for('home'))
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        users = dbHandler.retrieveUsers()
        x = (request.form['username'], request.form['password'])
        if x not in users:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You have logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/addUser', methods=['GET', 'POST'])
def addUser():
    error = None
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        users = dbHandler.retrieveUsers()

        x = request.form['username']
        print x

        for y in users:
            if x in y[0]:
                error = 'Username already exists. Please try again.'
                return render_template('addUser.html', error=error)

        else:
            dbHandler.addUser(username, password)
            session['logged_in'] = True
            return redirect(url_for('home'))

    else:

        return render_template('addUser.html',error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('login'))
