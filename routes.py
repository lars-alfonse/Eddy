import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from werkzeug.utils import secure_filename
from forms import LoginForm
import flask_sqlalchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from config import basedir

app = Flask(__name__)

app.config.from_object('config')
db = flask_sqlalchemy.SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)

import models

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


UPLOAD_FOLDER = '/static/music'
ALLOWED_EXTENSIONS = set(['wav'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('logout'))
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for username="%s", password="%s", remember_me=%s' %(form.username.data, form.password.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run(debug=True)
