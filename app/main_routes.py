# app/routes/main_routes.py
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """
    Render the homepage.

    Displays a cover image and generic information about the NFC Contact Share application.
    """
    return render_template('main/index.html')
