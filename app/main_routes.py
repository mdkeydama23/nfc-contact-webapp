# app/routes/main_routes.py
from flask import Blueprint, render_template, abort

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """
    Render the homepage.

    Displays a cover image and generic information about the NFC Contact Share application.
    """
    return render_template('main/index.html')


@main_bp.route('/', defaults={'path': ''})
@main_bp.route('/<path:path>')
def catch_all(path):
    """
    Catch all route to handle 404 errors for non-existent pages.

    Raises a NotFound exception for any URL that does not match existing routes.
    """
    # Raise a NotFound exception to trigger the 404 error handler
    abort(404)




# Error handlers

@main_bp.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404
 
@main_bp.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500

@main_bp.errorhandler(401)
def unauthorized_access(e):
    return render_template('error/401.html'), 401