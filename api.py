import os
import logging
from pyairtable import Api

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
API_KEY = os.environ.get('AIRTABLE_API_KEY')
BASE_KEY = os.environ.get('VERIC_BASE_KEY')
COMPANY_TABLE_KEY = os.environ.get('COMPANY_TABLE_KEY')
USERS_TABLE_KEY = os.environ.get('USERS_TABLE_KEY')
APPLICATIONS_TABLE_KEY = os.environ.get('APPLICATIONS_TABLE_KEY')

def check_env_vars():
    """
    Ensure all necessary environment variables are set.

    Raises:
        ValueError: If any required environment variable is missing.
    """
    required_vars = {
        'AIRTABLE_API_KEY': API_KEY,
        'VERIC_BASE_KEY': BASE_KEY,
        'COMPANY_TABLE_KEY': COMPANY_TABLE_KEY,
        'USERS_TABLE_KEY': USERS_TABLE_KEY,
        'APPLICATIONS_TABLE_KEY': APPLICATIONS_TABLE_KEY
    }

    missing_vars = [key for key, value in required_vars.items() if not value]
    if missing_vars:
        raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

check_env_vars()

if API_KEY is None:
    raise ValueError("API_KEY environment variable is not set.")

api = Api(API_KEY)


def init_table(api, base_key, table_key):
    """
    Initialize a table.

    Args:
        api (Api): The Airtable API client.
        base_key (str): The base key.
        table_key (str): The table key.

    Returns:
        Table: The initialized table.
    """
    return api.table(base_key, table_key)

# Initialize tables
company_table = init_table(api, BASE_KEY, COMPANY_TABLE_KEY)
users_table = init_table(api, BASE_KEY, USERS_TABLE_KEY)
applications_table = init_table(api, BASE_KEY, APPLICATIONS_TABLE_KEY)

def fetch_all_records(table):
    """
    Fetch all records from a given table.

    Args:
        table (Table): The table to fetch records from.

    Returns:
        list: A list of all records.
    """
    try:
        return table.all()
    except Exception as e:
        logger.error(f"Error fetching records from table {table.name}: {e}")
        return []

# Fetch all records from the tables
company_records = fetch_all_records(company_table)
users_records = fetch_all_records(users_table)
applications_records = fetch_all_records(applications_table)

def search_record_by_id(record_id):
    """
    Search for a record by ID in the company table.

    Args:
        record_id (str or list): The record ID(s) to search for.

    Returns:
        dict or list: The record(s) found or None if an error occurred.
    """
    try:
        if isinstance(record_id, list):
            return [company_table.get(id) for id in record_id]
        elif isinstance(record_id, str):
            return company_table.get(record_id)
        else:
            raise ValueError("record_id must be either a string or a list of strings")
    except Exception as e:
        logger.error(f"Error searching for record(s) with ID {record_id}: {e}")
        return None
