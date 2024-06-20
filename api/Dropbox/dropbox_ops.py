from ..env_config import DROPBOX_ACCESS_TOKEN, DROPBOX_REFRESH_TOKEN, DROPBOX_APP_KEY, DROPBOX_APP_SECRET
import dropbox
import dropbox.exceptions as dbx_exceptions
from ..logging_config import logger
import threading
import time
import requests

url = "https://api.dropboxapi.com/oauth2/token"
data = {
    "code": 'TYfPsXv02SAAAAAAAAAAhXeCp0vwLFLh373Ox24AgCw',
    "grant_type": "authorization_code",
    "client_id": DROPBOX_APP_KEY,
    "client_secret": DROPBOX_APP_SECRET,
}

def get_dropbox_client(access_token):
    """
    Returns a Dropbox client.
    """
    return dropbox.Dropbox(access_token)

def refresh_access_token():
    """
    Refreshes the Dropbox access token using the refresh token.
    """
    url = "https://api.dropbox.com/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": DROPBOX_REFRESH_TOKEN,
        "client_id": DROPBOX_APP_KEY,
        "client_secret": DROPBOX_APP_SECRET
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        logger.error(f"Failed to refresh access token: {response.text}")
        return None

def upload_file(file, file_name, delay=100):
    """
    Uploads a file to Dropbox and returns a shared link.

    Args:
        file: A file-like object to be uploaded.
        file_name: The name to give the file in Dropbox.
        delay: The delay in seconds before deleting the file (default: 100).

    Returns:
        A direct link to the uploaded file, or None if an error occurs.
    """
    MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB
    MIN_FILE_SIZE = 4  # 4 bytes

    access_token = DROPBOX_ACCESS_TOKEN
    dbx = get_dropbox_client(access_token)
    try:
        # Read the file content
        file_contents = file.read()
        file_size = len(file_contents)

        # Check file size constraints
        if not (MIN_FILE_SIZE <= file_size <= MAX_FILE_SIZE):
            logger.error(f"File size error: {file_size} bytes. Must be between 4 bytes and 500 MB.")
            return None

        logger.info(f"Uploading file {file_name} with size {file_size} bytes.")

        # Upload file to Dropbox
        dbx.files_upload(file_contents, '/' + file_name)

        # Create and return shared link
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(
            '/' + file_name
        )
        if shared_link_metadata is not None:
            shared_link = shared_link_metadata.url
            direct_link = shared_link.replace('dl=0', 'raw=1')

            logger.info(f"Shared link for {file_name}: {direct_link}")

            # Schedule file deletion
            threading.Thread(
                target=delete_file,
                args=(
                    file_name, delay
                )
            ).start()

            return direct_link
        else:
            return None

    except dbx_exceptions.AuthError as auth_err:
        logger.warning(f"Auth error: {auth_err}. Attempting to refresh access token.")
        new_access_token = refresh_access_token()
        if new_access_token:
            return upload_file(file, file_name, delay)  # Retry upload with new access token
        else:
            logger.error("Failed to refresh access token. Cannot proceed with upload.")
    except dbx_exceptions.ApiError as api_err:
        logger.error(f"Dropbox API error while uploading file {file_name}: {api_err}")
    except Exception as e:
        logger.error(f"An error occurred while uploading file {file_name}: {e}")
    return None

def delete_file(file_name, delay):
    """
    Deletes a file from Dropbox after a delay.

    Args:
        file_name: The name of the file to be deleted.
        delay: The delay in seconds before deleting the file.
    """
    try:
        time.sleep(delay)
        access_token = DROPBOX_ACCESS_TOKEN
        dbx = get_dropbox_client(access_token)
        dbx.files_delete('/' + file_name)
        logger.info(f"Deleted file {file_name} from Dropbox after {delay} seconds.")
    except dbx_exceptions.ApiError as api_err:
        logger.error(f"Dropbox API error while deleting file {file_name}: {api_err}")
    except Exception as e:
        logger.error(f"An error occurred while deleting file {file_name}: {e}")
