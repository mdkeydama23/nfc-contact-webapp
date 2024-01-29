from flask_login import UserMixin
from app import db, login_manager
from flask_bcrypt import Bcrypt
from sqlalchemy import DateTime
from sqlalchemy.orm import validates    

bcrypt = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
    """
    Callback function to reload the user object from the user ID stored in the session.

    Parameters:
    - user_id (int): User's unique identifier.

    Returns:
    - User: User object associated with the given user ID.
    """
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
    - username (str): User's username (unique).
    - password (str): User's hashed password.
    - role (str): User's role ('user' or 'admin', default is 'user').
    - tag_id (TagID): One-to-one relationship with TagID model.
    - contact_details (ContactDetails): One-to-one relationship with ContactDetails model.
    """
    __tablename__ = 'user'
    __table_args__ = (db.UniqueConstraint('user_id', 'email', name='unique_user_email'),)

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'

    tag_id = db.relationship('TagID', uselist=False, backref='user', lazy=True, cascade="all, delete-orphan")
    contact_details = db.relationship('ContactDetails', uselist=False, backref='user', lazy=True, cascade="all, delete-orphan")

    def is_admin(self):
        """
        Check if the user has an 'admin' role.

        Returns:
        - bool: True if the user is an admin, False otherwise.
        """
        return self.role == 'admin'

    def is_user(self):
        """
        Check if the user has a 'user' role.

        Returns:
        - bool: True if the user is a regular user, False otherwise.
        """
        return self.role == 'user'

    def get_id(self):
        """
        Get the user's unique identifier.

        Returns:
        - str: User's unique identifier.
        """
        return str(self.user_id)

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
    
    @validates('role')
    def validate_role(self, key, role):
        """
        Validate the user's role.

        Parameters:
        - key (str): Column name ('role').
        - role (str): User's role.

        Returns:
        - str: Validated user role.

        Raises:
        - ValueError: If an invalid role is provided.
        """
        if role not in ['user', 'admin']:
            raise ValueError("Invalid role. Must be 'user' or 'admin'.")
        return role

class ContactDetails(BaseModel):
    """
    ContactDetails model to store additional user information.

    Attributes:
    - contact_id (int): ContactDetails entry's unique identifier.
    - user_id (int): User ID associated with the contact details.
    - phone_number (str): User's phone number.
    - email (str): User's email address.
    - address (str): User's address.
    - photo_url (str): URL of the user's photo.
    - description (str): User's description or bio.
    - linkedin_profile_url (str): URL of the user's LinkedIn profile.
    - whatsapp_profile_url (str): URL of the user's WhatsApp profile.
    - telegram_profile_url (str): URL of the user's Telegram profile.
    - facebook_profile_url (str): URL of the user's Facebook profile.
    - instagram_profile_url (str): URL of the user's Instagram profile.
    """
    contact_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), unique=True)
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(255))
    address = db.Column(db.Text)
    photo_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    linkedin_profile_url = db.Column(db.String(255))
    whatsapp_profile_url = db.Column(db.String(255))
    telegram_profile_url = db.Column(db.String(255))
    facebook_profile_url = db.Column(db.String(255))
    instagram_profile_url = db.Column(db.String(255))

class TagID(BaseModel):
    """
    TagID model to represent NFC tag information.

    Attributes:
    - tag_id (str): NFC tag's unique identifier (UUID).
    - user_id (int): User ID associated with the NFC tag.
    - generated_at (datetime): Timestamp of when the tag was generated.
    """
    tag_id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), unique=True)
    generated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
