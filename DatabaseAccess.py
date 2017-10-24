import Pickler, models, SongData
from routes import db
from flask import g

def getSongs():
    user = g.user
    songs = []
    savedsongs = user.songs
    for data in savedsongs:
        song = Pickler.loadPickle(data.file)
        songs.append(song)
    return  songs


def saveSong(song, path):
    song.path= path
    pickle = Pickler.savePickle(song)
    dbsong =  models.Song()
    dbsong.seconds = song.seconds
    dbsong.path = path
    dbsong.name = song.name
    dbsong.file = pickle
    if not checkForSong(dbsong):
        db.session.add(dbsong)
    savedSong = db.session.query(models.Song).filter(models.Song.name == dbsong.name, models.Song.seconds == dbsong.seconds).first()
    if g.user:
        if g.user is not None and g.user.is_authenticated:
            g.user.songs.append(savedSong)
    for item in db.session.query(models.Song):
        print(item)
    db.session.commit()

def AddTrackChange(change):
    db.session.add(change)
    db.session.commit()

def checkForSong(dbsong):
    query = db.session.query(models.Song).filter(models.Song.name == dbsong.name, models.Song.seconds == dbsong.seconds)
    if query.count() > 0:
        return False
    else:
        return False

def getHistory():
    user = g.user
    query = db.session.query(models.TrackChange).filter(models.TrackChange.user_id == user.id)
    return query

def getSuggestions(pattern):
    query = db.session.query(models.TrackChange)
    matches = []
    for item in query:
        if item.pattern:
            if item.pattern in pattern:
                if item.currentTrack not in matches:
                    matches.append(item.currentTrack)
    return matches
