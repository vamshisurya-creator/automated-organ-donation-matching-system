import models
from app import app  # noqa: F401
# Initialize database when run through main.py as well
from database import db
from utils import populate_dummy_data

# This file is kept simple to ensure the run command works by default
# The actual application logic is in app.py


# Setup the database when run through main.py
with app.app_context():
    db.create_all()
    # Check if we need to populate with initial data
    if models.Admin.query.count() == 0:
        populate_dummy_data()
        print('Database initialized with sample data.')
