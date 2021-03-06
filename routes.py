import sqlite3
import datetime
import os
from flask import Flask, request, session, g, url_for, abort, \
     render_template, flash, redirect, jsonify
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

import models, SongProcessor, DatabaseAccess

@app.before_request
def before_request():
    g.user = current_user

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def home():
    songlist = []
    if request.method == 'POST':
        if 'file'not in request.files:
            flash('No file part')
            if g.user:
                if g.user is not None and g.user.is_authenticated:
                    songlist = DatabaseAccess.getSongs()
            return render_template('home.html', list=songlist)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            if g.user:
                if g.user is not None and g.user.is_authenticated:
                    songlist = DatabaseAccess.getSongs()
            return render_template('home.html', list = songlist)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            SongProcessor.process(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
            if g.user:
                if g.user is not None and g.user.is_authenticated:
                    songlist = DatabaseAccess.getSongs()
            return render_template('home.html', list=songlist)
    if g.user:
        if g.user is not None and g.user.is_authenticated:
            songlist = DatabaseAccess.getSongs()
    return render_template('home.html', list=songlist)

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
            return redirect(url_for('logout'))
    form = LoginForm()
    if form.validate_on_submit():
        if db.session.query(models.User).filter(models.User.username == form.username.data, models.User.password == form.password.data).count() > 0:
            login_user(db.session.query(models.User).filter(models.User.username == form.username.data, models.User.password == form.password.data).first(), remember=form.remember_me.data)
        return redirect('/index')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out')
    return redirect('/index')


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if db.session.query(models.User).filter(models.User.username == form.username.data).count() > 0:
            return render_template('register.html', title='Register', form=form)

        elif form.password.data != form.vpassword.data:
            return render_template('register.html', title='Register', form=form)

        else:
            db.session.add(models.User(username=form.username.data, password=form.password.data))
            db.session.commit()

        return redirect('login')
    return render_template('register.html', title='Register', form=form)

@app.route('/updateTrackHistory', methods=['POST','GET'])
def updateTrackHistory():
    if g.user:
        if g.user is not None and g.user.is_authenticated:
            user = g.user
            change = models.TrackChange()
            change.user_id = user.id
            change.currentTrack = request.args.get('currentSong', "", type=str)
            change.pattern = request.args.get('pattern', '', type=str)
            change.nextTrack = request.args.get('nextSong', "", type=str)
            change.startTime = request.args.get('startTime', 0.0, type=float)
            change.endTime = request.args.get('endTime', 0.0, type=float)
            change.timeOfChange = datetime.datetime.now()
            DatabaseAccess.AddTrackChange(change)
            return "success"

@app.route('/history')
def history():
    if g.user:
        if g.user is not None and g.user.is_authenticated:
            historyItems = DatabaseAccess.getHistory()
            return render_template('history.html', history=historyItems)
    else:
        return redirect('index')

@app.route('/trackInfo')
def trackInfo():
    if g.user:
        if g.user is not None and g.user.is_authenticated:
            tracks = DatabaseAccess.getSongs()
            return render_template('trackInfo.html', tracks=tracks)
    else:
        return redirect('index')

@app.route('/getTrackSuggestions', methods=['GET'])
def getTrackSuggestions():
    pattern = request.args.get('pattern', '', type=str)
    suggestions = DatabaseAccess.getSuggestions(pattern)
    return jsonify(tracks=suggestions)

if __name__ == '__main__':
    app.run(debug=True)
