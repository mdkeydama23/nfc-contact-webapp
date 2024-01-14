# app/tag_routes.py
from flask import Blueprint, flash, redirect, url_for
from app import db
from app.models import TagID, User
from app.user_routes import signup
import uuid

# Blueprint for tag-related routes
tag_bp = Blueprint('tag', __name__, url_prefix='/tag')

@tag_bp.route('/<uuid>')
def handle_tag(uuid):
    """
    Handle the /tag/uuid route.

    Check if the UUID exists in the TagID table and determine the action based on its association with a user.
    """
    tag = TagID.query.filter_by(tag_id=uuid).first()

    if not tag:
        flash('Invalid tag UUID. Please try again.', 'danger')
        return redirect(url_for('home'))

    if tag.user_id:
        # Tag is associated with a user, redirect to their contact details
        user = User.query.get(tag.user_id)
        return redirect(url_for('user.contact_details', username=user.username))
    else:
        # Tag is not associated with a user, redirect to sign-up page with UUID autofilled
        return signup(uuid=uuid)
