from .env_config import DROPBOX_ACCESS_TOKEN
import dropbox
from .logging_config import logger
import threading
import time

def upload_file(file, file_name):
    """
    Uploads a file to Dropbox and returns a shared link.

    Args:
        file: A file-like object to be uploaded.
        file_name: The name to give the file in Dropbox.

    Returns:
        A direct link to the uploaded file, or None if an error occurs.
    """
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

        # Read the file content
        file_contents = file.read()
        logger.info(f"Uploading file {file_name} with size {len(file_contents)} bytes.")

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
                    file_name, 100
                    )
            ).start()

            return direct_link
        else:
            return None

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
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        dbx.files_delete('/' + file_name)
        logger.info(f"Deleted file {file_name} from Dropbox after {delay} seconds.")
    except Exception as e:
        logger.error(f"An error occurred while deleting file {file_name}: {e}")

