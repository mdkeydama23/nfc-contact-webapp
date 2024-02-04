# app.py
from app import create_app, db
from flask_migrate import Migrate, upgrade

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

