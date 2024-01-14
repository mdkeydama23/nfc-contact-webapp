# app/models.py

from flask_login import UserMixin
from app import db, login_manager
from flask_bcrypt import Bcrypt
from sqlalchemy import DateTime

bcrypt = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
    # This callback is used to reload the user object from the user ID stored in the session
    return User.query.get(int(user_id))

class BaseModel(db.Model):
    """
    Base model to handle common fields for all database models.

    Attributes:
    - created_at (DateTime): Timestamp of when the record was created.
    - updated_at (DateTime): Timestamp of when the record was last updated.
    """
    __abstract__ = True
    created_at = db.Column(DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class User(BaseModel, UserMixin):
    """
    User model to represent user information.

    Attributes:
    - user_id (int): User's unique identifier.
    - first_name (str): User's first name.
    - last_name (str): User's last name.
    - email (str): User's email address (unique).
    - password (str): User's hashed password.
    """
    __tablename__ = 'user'
    __table_args__ = (db.UniqueConstraint('user_id', 'email', name='unique_user_email'),)
    
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    # Add other general user details as needed

    # Flask-Login methods
    def get_id(self):
        """
        Get the user's unique identifier.

        Returns:
        - str: User's unique identifier.
        """
        return str(self.user_id)

    # Bcrypt methods
    def set_password(self, password):
        """
        Set the user's password by hashing it.

        Parameters:
        - password (str): Plain text password.
        """
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """
        Check if the provided password matches the stored hashed password.

        Parameters:
        - password (str): Plain text password.

        Returns:
        - bool: True if the passwords match, False otherwise.
        """
        return bcrypt.check_password_hash(self.password, password)

class ContactDetails(BaseModel):
    """
    ContactDetails model to store additional user information.

    Attributes:
    - contact_id (int): ContactDetails entry's unique identifier.
    - user_id (int): User ID associated with the contact details.
    - phone_number (str): User's phone number.
    - address (str): User's address.
    - photo_url (str): URL of the user's photo.
    - description (str): User's description or bio.
    """
    contact_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    phone_number = db.Column(db.String(20))
    address = db.Column(db.Text)
    photo_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    # Add other contact details as needed

class AdminUser(BaseModel, UserMixin):
    """
    AdminUser model to represent admin user information.

    Attributes:
    - admin_id (int): Admin user's unique identifier.
    - username (str): Admin user's username.
    - email (str): Admin user's email address (unique).
    - password (str): Admin user's hashed password.
    """
    __tablename__ = 'admin_user'
    __table_args__ = (db.UniqueConstraint('admin_id', 'email', name='unique_admin_email'),)

    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    # Add other admin user details as needed

    # Flask-Login methods
    def get_id(self):
        """
        Get the admin user's unique identifier.

        Returns:
        - str: Admin user's unique identifier.
        """
        return str(self.admin_id)

    # Bcrypt methods
    def set_password(self, password):
        """
        Set the admin user's password by hashing it.

        Parameters:
        - password (str): Plain text password.
        """
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """
        Check if the provided password matches the stored hashed password.

        Parameters:
        - password (str): Plain text password.

        Returns:
        - bool: True if the passwords match, False otherwise.
        """
        return bcrypt.check_password_hash(self.password, password)

class TagID(BaseModel):
    """
    TagID model to represent NFC tag information.

    Attributes:
    - tag_id (str): NFC tag's unique identifier (UUID).
    - user_id (int): User ID associated with the NFC tag.
    - generated_at (datetime): Timestamp of when the tag was generated.
    """
    tag_id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    generated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
