# app/tag_routes.py

from flask import Blueprint, flash, redirect, url_for, render_template
from app.models import TagID

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
        return redirect(url_for('user.contact_details', tag_id=tag.tag_id))
    else:
        # Tag is not associated with a user, redirect to sign-up page with UUID autofilled
        return redirect(url_for('user.signup', uuid=tag.tag_id))
