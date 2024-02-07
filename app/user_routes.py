# app/user_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models import User, TagID, ContactDetails
from functools import wraps

# Blueprint for user-related routes
user_bp = Blueprint('user', __name__, url_prefix='/user')

# Decorator to require admin access
def user_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_user():
            flash('You are not authorized to access this page.', 'danger')
            return render_template('error/401.html'), 401
        return func(*args, **kwargs)
    return decorated_function





@user_bp.route('/contact_details/<tag_id>')
def contact_details(tag_id):
    """
    Render the contact details for the logged-in user or the user associated with the provided username.

    Does not require the user to be logged in.
    """
    # Retrieve the user based on the provided username or use the logged-in user
    tag = TagID.query.filter_by(tag_id=tag_id).first()
    user = User.query.filter_by(user_id=tag.user_id).first()

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('main.home'))

    # Check if the user has associated contact details
    contact_details = ContactDetails.query.filter_by(user_id=user.user_id).first()

    return render_template('user/contact_details.html', user=user, contact_details=contact_details)


@user_bp.route('/signup/<uuid>')
def signup(uuid):
    """
    Handle the user signup process.

    If the form is submitted, validate the input and create a new user.
    """


    if current_user.is_authenticated:
        if current_user.is_user():
            tag = TagID.query.filter_by(user_id=current_user.user_id).first()

            if tag.tag_id == uuid:
                flash('You have already registered!', 'danger')
                return redirect(url_for('user.dashboard'))
            
            if tag.tag_id != uuid:
                flash('The tag ID does not match the user!', 'danger')
                logout_user()
                return redirect(url_for('user.signup', uuid=uuid))  

            return redirect(url_for('user.dashboard'))
        
        else:
            flash('You are not authorized to access this page.', 'danger')
            return render_template('error/401.html'), 401
        
    else:
        return render_template('user/signup.html', uuid=uuid)
    

@user_bp.route('/signup_form', methods=['POST'])
def signup_form():
    """ 
    Handle the form submission for user signup.
    
    """
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
        db.session.commit() 

        # Associate tag with user (UUID)
        tag = TagID.query.filter_by(tag_id=uuid).first()
        tag.user_id = new_user.user_id
        
        db.session.add(tag)
        db.session.commit()
        
        flash('User created successfully!', 'success')

        # Log in the newly created user
        login_user(new_user)

        return redirect(url_for('user.dashboard'))


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.

    If the user is already authenticated, redirect to the user dashboard.
    If the form is submitted, validate the credentials and log in the user.
    """
    if current_user.is_authenticated:
        if current_user.is_user():
            tag = TagID.query.filter_by(user_id=current_user.user_id).first()
            return redirect(url_for('user.contact_details', tag_id=tag.tag_id))
        else:
            flash('You are not authorized to access this page.', 'danger')
            return render_template('error/401.html'), 401

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()



        if user and user.check_password(password=password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('user.dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('user/login.html')


@user_bp.route('/dashboard', methods=['GET', 'POST'])
@user_required
@login_required
def dashboard():
    """
    Render the user dashboard.

    Displays options for editing contact details and other user-related actions.
    Requires the user to be logged in.
    """

    contact_details = ContactDetails.query.filter_by(user_id=current_user.user_id).first()
    
    return render_template('user/dashboard.html', user=current_user, contact_details=contact_details )


@user_bp.route('/edit_contact_details', methods=['POST'])
@user_required  
@login_required
def edit_contact_details():
    """
    Handle the form submission for editing contact details.

    Update the contact details in the database.
    Requires the user to be logged in.
    """

    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        description = request.form.get('description')
        linkedin_profile_url = request.form.get('linkedin_profile_url')
        whatsapp_profile_url = request.form.get('whatsapp_profile_url')
        facebook_profile_url = request.form.get('facebook_profile_url')

        # Update contact details in the database
        contact_details = ContactDetails.query.filter_by(user_id=current_user.user_id).first()

        if contact_details:
            pass
        else:
            contact_details = ContactDetails(user_id=current_user.user_id)

        contact_details.phone_number = phone_number
        contact_details.address = address
        contact_details.description = description
        contact_details.linkedin_profile_url = linkedin_profile_url
        contact_details.whatsapp_profile_url = whatsapp_profile_url
        contact_details.facebook_profile_url = facebook_profile_url
        
        db.session.add(contact_details)
        db.session.commit()
        
        flash('Contact details updated successfully!', 'success')
    


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
        


def check_validity_email(email):
    
    # Check if the email is already taken
    if User.query.filter_by(email=email).first():
        flash('Email is already taken. Please choose another.', 'danger')
