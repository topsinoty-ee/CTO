from .Dropbox.dropbox_ops import upload_file
from .logging_config import logging
import re
import json
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


def CRUD(table, record_id: Optional[str] = None, data: Optional[Dict[str, Any]] = None, 
     files: Optional[Dict[str, Any]] = None, option: str = 'read') -> Optional[Dict[str, Any]]:
    """
    Perform CRUD operations on a specified table.
    
    Args:
        table (Table): The Airtable table instance.
        record_id (str): The ID of the record for read, update, or delete operations.
        data (dict): The data for create or update operations.
        files (dict): The files for create or update operations.
        option (str): The CRUD operation to perform: 'create', 'read', 'update', or 'delete'.
    
    Returns:
        dict or None: The result of the CRUD operation, or None if an error occurred.
    """
    try:
        option = option.lower()
        if option in ['create', 'post', 'update']:
            if option == 'create' and data is None:
                raise ValueError("Data must be provided to create a record.")
            if option == 'update' and (record_id is None or data is None):
                raise ValueError("Record ID and data must be provided to update a record.")
    
            # Handle file uploads
            uploaded_files = {}
            if files:
                for key, file in files.items():
                    try:
                        shared_link = upload_file(file, file.filename)
                        if shared_link:
                            uploaded_files[key] = [{'url': shared_link}]
                        else:
                            logger.warning(f"Failed to upload file: {file.filename}")
                    except Exception as e:
                        logger.warning(f"Exception occurred while uploading file {file.filename}: {e}")
    
            # Merge data and file links
            data_with_files = {**(data or {}), **uploaded_files}
            logger.info(f"Data with files: {data_with_files}")
    
            if option in ['create', 'post']:
                record = table.create(data_with_files)
                logger.info(f"Created record with ID: {record['id']}")
            else:  # option == 'update'
                record = table.update(record_id, data_with_files)
                logger.info(f"Updated record with ID: {record['id']}")
    
            return record
    
        elif option in ['read', 'get']:
            if record_id is None:
                raise ValueError("Record ID must be provided to read a record.")
            record = table.get(record_id)
            logger.info(f"Read record with ID: {record['id']}")
            return record
    
        elif option == 'delete':
            if record_id is None:
                raise ValueError("Record ID must be provided to delete a record.")
            table.delete(record_id)
            logger.info(f"Deleted record with ID: {record_id}")
            return {'status': 'deleted'}
    
        else:
            raise ValueError("Invalid CRUD option provided. Choose from 'create', 'read', 'update', 'delete'.")
    
    except Exception as e:
        logger.error(f"Error during {option} operation: {e}")
        return None
def convert_to_json(input_string):
    """
    Converts a string to a valid JSON string.

    Args:
        input_string (str): A string.

    Returns:
        str: A valid JSON string.
    """
    # Replace single quotes with double quotes
    json_string = input_string.replace("'", '"')
    json_string = re.sub(r'\bTrue\b', 'true', json_string)
    json_string = re.sub(r'\bFalse\b', 'false', json_string)
    json_string = re.sub(r'\bNone\b', 'null', json_string)
    try:
        json_obj = json.loads(json_string)
        return json_obj
    except json.JSONDecodeError as e:
        return (f"Invalid JSON string: {e}")
