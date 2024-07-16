import threading
import time
from dropbox import Dropbox, exceptions
from ..env_config import DROPBOX_ACCESS_TOKEN, DROPBOX_APP_KEY, DROPBOX_APP_SECRET
from ..logging_config import logging
# from .get_token import refresh_dropbox_token

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB
MIN_FILE_SIZE = 4  # 4 bytes

def get_dropbox_client(access_token):
    return Dropbox(access_token)

def upload_file(file, file_name, delay=100):
    access_token = DROPBOX_ACCESS_TOKEN
    dbx = get_dropbox_client(access_token)

    try:
        file_contents = file.read()
        file_size = len(file_contents)

        if not (MIN_FILE_SIZE <= file_size <= MAX_FILE_SIZE):
            logger.error(f"File size error: {file_size} bytes. Must be between 4 bytes and 500 MB.")
            return None

        logger.info(f"Uploading file {file_name} with size {file_size} bytes.")

        dbx.files_upload(file_contents, '/' + file_name)

        shared_link_metadata = dbx.sharing_create_shared_link_with_settings('/' + file_name)
        if shared_link_metadata:
            shared_link = shared_link_metadata.url
            direct_link = shared_link.replace('dl=0', 'raw=1')

            logger.info(f"Shared link for {file_name}: {direct_link}")

            threading.Thread(target=delete_file, args=(file_name, delay)).start()

            return direct_link
        else:
            return None

    except exceptions.AuthError as auth_err:
        logger.warning(f"Auth error: {auth_err}. Attempting to refresh access token.")
        new_access_token = "" #refresh_dropbox_token()
        if new_access_token:
            return upload_file(file, file_name, delay)  # Retry upload with new access token
        else:
            logger.error("Failed to refresh access token. Cannot proceed with upload.")
    except exceptions.ApiError as api_err:
        logger.error(f"Dropbox API error while uploading file {file_name}: {api_err}")
    except Exception as e:
        logger.error(f"An error occurred while uploading file {file_name}: {e}")

    return None

def delete_file(file_name, delay):
    try:
        time.sleep(delay)
        access_token = DROPBOX_ACCESS_TOKEN
        dbx = get_dropbox_client(access_token)
        dbx.files_delete('/' + file_name)
        logger.info(f"Deleted file {file_name} from Dropbox after {delay} seconds.")
    except exceptions.ApiError as api_err:
        logger.error(f"Dropbox API error while deleting file {file_name}: {api_err}")
    except Exception as e:
        logger.error(f"An error occurred while deleting file {file_name}: {e}")

