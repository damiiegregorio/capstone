from config import db, app
from models import File
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

# Create the database
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

if not database_exists(engine.url):
    # Create database
    create_database(engine.url, encoding='utf8', template="template0")

    # Create FILE TABLE
    db.create_all()
    db.session.commit()
else:

    # Create FILE TABLE
    db.create_all()
    db.session.commit()