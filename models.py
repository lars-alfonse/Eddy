from routes import db


association_table = db.Table('association', db.Model.metadata, db.Column('user_id', db.Integer, db.ForeignKey('user.id')), db.Column('song_id', db.Integer, db.ForeignKey('song.id')))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=True, unique=False)
    email = db.relationship('Email', backref='user', lazy=False, uselist=False)
    songs = db.relationship("Song", secondary=association_table)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Email %r>' % (self.email)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    seconds = db.Column(db.Integer)
    path = db.Column(db.String(200), unique=True)
    file = db.Column(db.LargeBinary)

class TrackChange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currentTrack = db.Column(db.String(100))
    endTime = db.Column(db.Float)
    pattern = db.Column(db.String(10))
    nextTrack = db.Column(db.String(100))
    startTime = db.Column(db.Float)
    timeOfChange =  db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
