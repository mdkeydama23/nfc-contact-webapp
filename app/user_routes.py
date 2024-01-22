# app/user_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models import User, TagID, ContactDetails

# Blueprint for user-related routes
user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/contact_details/<user_id>')
def contact_details(user_id):
    """
    Render the contact details for the logged-in user or the user associated with the provided username.

    Does not require the user to be logged in.
    """
    # Retrieve the user based on the provided username or use the logged-in user
    user = User.query.filter_by(user_id=user_id).first() or current_user

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('user.signup'))

    # Check if the user has associated contact details
    contact_details = ContactDetails.query.filter_by(user_id=user.user_id).first()

    return render_template('user/contact_details.html', user=user, contact_details=contact_details)


@user_bp.route('/signup/<uuid>', methods=['GET', 'POST'])
@user_bp.route('/signup', methods=['GET', 'POST'])
def signup(uuid=None):
    """
    Handle the user signup process.

    If the form is submitted, validate the input and create a new user.
    """
    if current_user.is_authenticated:
        return redirect(url_for('user.user_dashboard', username=current_user.username))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        uuid = request.form.get('uuid')

        # Check if the username is already taken
        check_validity_username(username)

        # Check if the email is already taken
        check_validity_email(email)

        # Create a new user and associate a tag ID with the user
        new_user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        db.session.add(new_user)

        # Generate a unique tag (UUID)
        tag = TagID.query.filter_by(tag_id=uuid).first()
        tag.user_id = new_user.user_id
        
        db.session.commit()
        
        flash('User created successfully!', 'success')

        # Log in the newly created user
        login_user(new_user)

        contact_details = ContactDetails(user_id=new_user.user_id) 

        return redirect(url_for('user.dashboard', username=username, contact_details=contact_details))
    
    if uuid is not None:
        return render_template('user/signup.html', uuid=uuid)
    
    return render_template('user/signup.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.

    If the user is already authenticated, redirect to the user dashboard.
    If the form is submitted, validate the credentials and log in the user.
    """
    if current_user.is_authenticated:
        return redirect(url_for('user.contact_details', username=current_user.username))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        contact_details = ContactDetails(user_id=user.user_id) 


        if user and user.check_password(password=password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('user.dashboard', username=user.username, contact_details=contact_details))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('user/login.html')


@user_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Render the user dashboard.

    Displays options for editing contact details and other user-related actions.
    Requires the user to be logged in.
    """

    contact_details = ContactDetails(user_id=current_user.user_id)
    
    return render_template('user/dashboard.html', user=current_user, contact_details=contact_details )


user_bp.route('/edit_contact_details', methods=['POST'])
@login_required
def edit_contact_details():
    """
    Handle the form submission for editing contact details.

    Update the contact details in the database.
    Requires the user to be logged in.
    """
    user = current_user

    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        # Add other contact details fields as needed

        # Update contact details in the database
        contact_details = ContactDetails.query.filter_by(user_id=user.user_id).first()
        if contact_details:
            contact_details.phone_number = phone_number
            contact_details.address = address
            # Update other contact details fields as needed
            db.session.commit()
            flash('Contact details updated successfully!', 'success')
        else:
            flash('Contact details not found.', 'danger')

    return redirect(url_for('user.dashboard'))




@user_bp.route('/logout')
@login_required
def logout():
    """
    Handle user logout.

    Log out the currently logged-in user.
    """
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('main.home'))




# Helper functions

def check_validity_username(username):
    
    # Check if the username is already taken
    if User.query.filter_by(username=username).first():
        flash('Username is already taken. Please choose another.', 'danger')
        return redirect(url_for('user.signup'))


def check_validity_email(email):
    
    # Check if the email is already taken
    if User.query.filter_by(email=email).first():
        flash('Email is already taken. Please choose another.', 'danger')
        return redirect(url_for('user.signup'))