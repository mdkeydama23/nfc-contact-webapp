from app import create_app, db
app = create_app()
with app.app_context():

# Create the database tables
    db.create_all()

print('Database tables created succesfully.')