import sqlite3
import os
from flask import Flask, request, session, g, url_for, abort, \
     render_template, flash, redirect
from werkzeug.utils import secure_filename
from forms import LoginForm, RegisterForm
import flask_sqlalchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from config import basedir


app = Flask(__name__)

app.config.from_object('config')
db = flask_sqlalchemy.SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)

import models

@app.before_request
def before_request():
    g.user = current_user

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


UPLOAD_FOLDER = '/static/music'
ALLOWED_EXTENSIONS = set(['wav'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@lm.user_loader
def load_user(id):
    return models.User.query.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        if g.user is not None and g.user.is_authenticated:
            return redirect(url_for('index'))
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


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if db.session.query(models.User).filter(models.User.username == form.username).count() > 0:
            return render_template('register.html', title='Register', form=form)

        elif form.password != form.vpassword:
            return render_template('register.html', title='Register', form=form)

        else:
            db.session.add(models.User(username=form.username, password=form.password))
            db.session.commit()

        return redirect('login')
    return render_template('register.html', title='Register', form=form)


if __name__ == '__main__':
    app.run(debug=True)
