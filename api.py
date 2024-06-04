import bcrypt
from logging import debug, getLogger, basicConfig, INFO
import os
from pyairtable import Api
from pyairtable.api.table import Table

# Set up logging
basicConfig(level=INFO)
logger = getLogger(__name__)

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

# Check environment variables
check_env_vars()

if API_KEY is None:
    raise ValueError("API_KEY environment variable is not set.")

# Initialize Airtable API client
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
        table (Table): The table from which to fetch records.

    Returns:
        list: List of records fetched from the table, or an empty list if an error occurred.
    """
    try:
        records = table.all()
        logger.info(f"Fetched {len(records)} records from {table.name}")
        return records
    except Exception as e:
        logger.error(f"Error fetching records from table {table.name}: {e}")
        return []

# Fetch all records from the tables
company_records = fetch_all_records(company_table)
users_records = fetch_all_records(users_table)
applications_records = fetch_all_records(applications_table)

def search_record_by_id(table, record_id):
    """
    Search for a record by ID in a specified table.

    Args:
        table (Table): The table to search.
        record_id (str or list): The record ID(s) to search for.

    Returns:
        dict or list: The record(s) found or None if an error occurred.
    """
    try:
        if isinstance(record_id, list):
            records = [CRUD(table, record_id=id, option='read') for id in record_id]
            return records
        elif isinstance(record_id, str):
            return CRUD(table, record_id=record_id, option='read')
        else:
            raise ValueError("record_id must be either a string or a list of strings")
    except Exception as e:
        logger.error(f"Error searching for record(s) with ID {record_id}: {e}")
        return None


def sign_up_as_company(email, password, company_name):
    """
    Sign up a new company.

    Args:
        email (str): The email address of the company.
        password (str): The password for the company account.
        company_name (str): The name of the company.

    Returns:
        dict: The created company record, or None if an error occurred.
    """
    try:
        # Input validation
        if not email or not password or not company_name:
            raise ValueError("Email, password, and company name must be provided.")

        # Check if the email is already in use
        existing_company = CRUD(company_table, option='read', record_id=email)
        if existing_company:
            raise ValueError("A company with this email already exists.")

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        logger.info(f"Hashed password for {email}")

        # Create the company record
        company_record = CRUD(
            table=company_table,
            data={
                'email': email,
                'password': hashed_password.decode('utf-8'),
                'name': company_name
            },
            option='create'
        )

        logger.info(f"Created company record with ID: {company_record['id']}")
        return company_record

    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
    except Exception as e:
        logger.error(f"Error creating new company: {e}")
    return None


def login_as_company(email, password):
    """
    Log in as a company.

    Args:
        email (str): The email address of the company.
        password (str): The password for the company account.

    Returns:
        dict: The authenticated company record, or None if authentication failed.
    """
    try:
        # Search for company by email
        formula = f"{{email}} = '{email}'"
        companies_records = CRUD(company_table, data={'formula': formula}, option='read')

        if not companies_records:
            logger.warning(f"No company found with email: {email}")
            return None

        company = companies_records[0]['fields']

        # Check password
        if bcrypt.checkpw(password.encode('utf-8'), company['password'].encode('utf-8')):
            logger.info(f"Company logged in: {email}")
            return company

        logger.warning(f"Invalid password for company: {email}")
        return None
    except Exception as e:
        logger.error(f"Error authenticating account '{email}': {e}")
        return None


def CRUD(table, record_id=None, data=None, option='read'):
    """
    Perform CRUD operations on a specified table.

    Args:
        table (Table): The Airtable table instance.
        record_id (str): The ID of the record for read, update, or delete operations.
        data (dict): The data for create or update operations.
        option (str): The CRUD operation to perform: 'create', 'read', 'update', or 'delete'.

    Returns:
        dict or None: The result of the CRUD operation, or None if an error occurred.
    """
    try:
        if option == 'create':
            if data is None:
                raise ValueError("Data must be provided to create a record.")
            record = table.create(data)
            logger.info(f"Created record with ID: {record['id']}")
            return record

        elif option == 'read':
            if record_id is None:
                raise ValueError("Record ID must be provided to read a record.")
            record = table.get(record_id)
            logger.info(f"Read record with ID: {record['id']}")
            return record

        elif option == 'update':
            if record_id is None or data is None:
                raise ValueError("Record ID and data must be provided to update a record.")
            record = table.update(record_id, data)
            logger.info(f"Updated record with ID: {record['id']}")
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
