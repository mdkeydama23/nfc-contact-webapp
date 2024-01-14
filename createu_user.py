# create_admin.py
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Create a dummy user
    dummy_user = User(username='dummy_user', email='dummy@example.com', first_name='Dummy', last_name='User')

    # Hash the password and store it
    dummy_user.set_password('password')

    # Add the dummy user to the session and commit it to the database
    db.session.add(dummy_user)
    db.session.commit()

print("Dummy user created successfully!")