from app import create_app, db
app = create_app()
app.app_context().push()

# Create the database tables
db.create_all()