# create_admin.py
from app import create_app, db
from app.models import User, TagID

app = create_app()

with app.app_context():
    # Create a dummy user
    user = User(username='dummy', password='dummy', email="---x@xxxxxxx.xxx", role='user')

print("Dummy user created successfully!")