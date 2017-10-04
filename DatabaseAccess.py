import Pickler, models, SongData
from routes import db
from flask import g










def getSongs():
    user = g.user
    songs = []
    savedsongs = user.songs.all()
    for data in savedsongs:
        song = Pickler.loadPickle(data.file)
        songs.append(song)
    return  songs


def saveSong(song):
    pickle = Pickler.savePickle(song)
    dbsong =  models.Song()
    dbsong.seconds = song.seconds
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






def checkForSong(dbsong):
    query = db.session.query(models.Song).filter(models.Song.name == dbsong.name, models.Song.seconds == dbsong.seconds)
    if query.count() > 0:
        return True
    else:
        return False