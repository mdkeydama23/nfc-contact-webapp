# app/tag_routes.py

from flask import Blueprint, flash, redirect, url_for, render_template
from app.models import TagID, User, ContactDetails
from app.user_routes import signup

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
        return render_template('tags/invalid_tag.html')

    if tag.user_id:
        # Tag is associated with a user, redirect to their contact details
        user = User.query.get(tag.user_id)
        contact_details = ContactDetails.query.filter_by(user_id=user.user_id).first()

        return redirect(url_for('user.contact_details', user_id=tag.user_id, contact_details=contact_details))
    else:
        # Tag is not associated with a user, redirect to sign-up page with UUID autofilled
        return signup(uuid=uuid)
