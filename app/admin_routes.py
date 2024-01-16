# app/admin_routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user
from app import db
from app.models import AdminUser, TagID
import uuid

# Blueprint for admin-related routes
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle admin login.

    If the admin is already authenticated, redirect to the admin dashboard.
    If the form is submitted, validate the credentials and log in the admin.
    """
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin_user = AdminUser.query.filter_by(username=username).first()

        if admin_user and admin_user.check_password(password):
            login_user(admin_user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('admin/login.html')


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Render the admin dashboard.

    Displays a button to generate a new tag and lists previously generated tags.
    Requires the admin to be logged in.
    """
    # Retrieve the list of generated tags for the admin user
    tags = TagID.query.all()
    return render_template('admin/dashboard.html', tags=tags)


@admin_bp.route('/generate_tag')
@login_required
def generate_tag():
    """
    Generate a unique tag (UUID) and associate it with the tag_id.

    Redirect to the admin dashboard after generating the tag.
    """
    # Generate a unique tag (UUID)
    unique_tag = str(uuid.uuid4())
    
    # Create a new TagID entry in the database without associating it with any user
    new_tag = TagID(tag_id=unique_tag)
    db.session.add(new_tag)
    db.session.commit()

    flash(f'Tag generated successfully: {unique_tag}', 'success')
    return redirect(url_for('admin.dashboard'))
