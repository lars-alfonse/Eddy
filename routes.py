import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from werkzeug.utils import secure_filename
from forms import LoginForm
import flask_sqlalchemy

app = Flask(__name__)

app.config.from_object('config')
db = flask_sqlalchemy.SQLAlchemy(app)

import models

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


UPLOAD_FOLDER = '/static/music'
ALLOWED_EXTENSIONS = set(['wav'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for username="%s", password="%s", remember_me=%s' %(form.username.data, form.password.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run(debug=True)
