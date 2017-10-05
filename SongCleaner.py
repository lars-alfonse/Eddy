import models
from routes import db

try:
    db.session.query(models.Song).delete()
    db.session.commit()
except:
    db.session.rollback()
