# create_admin.py
from app import create_app, db
from app.models import AdminUser

app = create_app()

with app.app_context():
    # Create a new instance of AdminUser
    admin = AdminUser(username='chuchu', email='zendro@example.com')

    # Hash the password and store it
    admin.set_password('password')

    # Add the new admin to the session and commit it to the database
    db.session.add(admin)
    db.session.commit()

print("Admin user created successfully!")