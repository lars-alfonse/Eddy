from routes import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=True, unique=False)
    email = db.relationship('email', backref='user', lazy=False, uselist=False)
    def __repr__(self):
        return '<User %r>' % (self.username)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Email %r>' % (self.email)


