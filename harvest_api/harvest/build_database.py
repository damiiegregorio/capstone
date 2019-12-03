from config import db
from models import File

# Data to initialize database with
# Create the database
db.create_all()

db.session.commit()
