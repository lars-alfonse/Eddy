from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
track_change = Table('track_change', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('currentTrack', String(length=100)),
    Column('endTime', Float),
    Column('nextTrack', String(length=100)),
    Column('startTime', Float),
    Column('timeOfChange', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['track_change'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['track_change'].drop()
