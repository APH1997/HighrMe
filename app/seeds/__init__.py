from flask.cli import AppGroup
from .users import seed_users, undo_users
from .photos import seed_photos, undo_photos
from .albums import seed_albums, undo_albums
from .comments import seed_comments, undo_comments
from .replies import seed_replies, undo_replies

from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')

# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Before seeding in production, you want to run the seed undo
        # command, which will  truncate all tables prefixed with
        # the schema name (see comment in users.py undo_users function).
        # Make sure to add all your other model's undo functions below

        undo_replies()
        undo_comments()
        undo_albums()
        undo_photos()
        undo_users()
    all_users = seed_users()
    all_pics = seed_photos()
    seed_albums(all_pics)
    all_comments = seed_comments(all_users, all_pics)
    seed_replies(all_comments, all_users)


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_replies()
    undo_comments()
    undo_albums()
    undo_photos()
    undo_users()
    # Add other undo functions here
