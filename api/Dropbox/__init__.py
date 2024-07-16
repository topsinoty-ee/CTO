from flask import Blueprint, session
from flask.helpers import redirect
from ..logging_config import logging

logger = logging.getLogger(__name__)

dropbox_ops_bp = Blueprint('dropbox_ops', __name__)

@dropbox_ops_bp.route('/oauth2?next=<next_url>', methods=['GET'])
def oauth2(next_url):
    """
    Handle the OAuth2 flow for Dropbox.

    Args:
        next_url (str): The URL to redirect to after successful authentication.

    Returns:
        str: Rendered HTML template for the Dropbox OAuth2 flow.
    """
    session['next_url'] = next_url
    logger.info(
        f'session["next"] = {session["next"]}'
    )

    
    logger.info(f'Redirecting to Dropbox OAuth2 flow with next_url: {next_url}')
    return redirect(next_url)