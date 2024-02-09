# create_admin.py
from app import create_app, db
from app.models import User, TagID

app = create_app()

with app.app_context():
    # Create a dummy user
   tag_id = TagID(tag_id='1234567890', user_id=1)

print("Dummy user created successfully!")