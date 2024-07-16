import os
import re
import dropbox
import dropbox.exceptions
from dropbox.oauth import DropboxOAuthedClient
import os

from api.env_config import REDIRECT_URI

APP_KEY = os.environ['DROPBOX_APP_KEY']
APP_SECRET = os.environ['DROPBOX_APP_SECRET']
TOKEN_FILE = 'api/Dropbox/dropbox-access-token.txt'
REFRESH_FILE = 'api/Dropbox/dropbox-refresh-token.txt'

def authenticate():
    auth_flow = DropboxOAuth2(APP_KEY, APP_SECRET, token_access_type='offline', REDIRECT_URI)
    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print("2. Click 'Allow' (you might have to log in first)")
    print("3. Copy the authorization code.")
    auth_code = input("Enter the authorization code here: ").strip()

    try:
        oauth_result = auth_flow.finish(auth_code)
        with open(TOKEN_FILE, 'w') as token_file:
            token_file.write(oauth_result.access_token)

        with open(REFRESH_FILE, 'w') as refresh_file:
            refresh_file.write(oauth_result.refresh_token)
        return oauth_result
        
    except Exception as e:
        print('Error: %s' % (e, ))
        return None


def get_dropbox_client():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as token_file:
            access_token = token_file.read().strip()
    else:
        access_token = authenticate()

    if not access_token:
        print("Failed to obtain access token.")
        return None

    dbx = dropbox.Dropbox(access_token)

    # Test the connection
    try:
        user = dbx.users_get_current_account()
        print("Successfully connected to Dropbox. User:",
              user.name.display_name)
    except dropbox.exceptions.AuthError as e:
        print("Error connecting to Dropbox:", e)
        return None

    return dbx


authenticate()
get_dropbox_client()