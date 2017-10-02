from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user_emails = Table('user_emails', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('email_id', INTEGER),
)

email = Table('email', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('email', String(length=100)),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user_emails'].drop()
    post_meta.tables['email'].columns['user_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user_emails'].create()
    post_meta.tables['email'].columns['user_id'].drop()
