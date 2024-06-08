from pyairtable import Api
from pyairtable.api.table import Table
from .env_config import (
    API_KEY,
    BASE_KEY,
    COMPANY_TABLE_KEY,
    USERS_TABLE_KEY,
    APPLICATIONS_TABLE_KEY
)
from .logging_config import logger
from .utils import CRUD


if API_KEY is None:
    raise ValueError("API_KEY environment variable is not set.")

# Initialize Airtable API client
api = Api(API_KEY)


def init_table( table_key) -> Table:
    """
    Initialize a table.

    Args:
        api (Api): The Airtable API client.
        base_key (str): The base key.
        table_key (str): The table key.

    Returns:
        Table: The initialized table.
    """
    if BASE_KEY is None:
        raise ValueError("BASE_KEY environment variable is not set.")
    return api.table(BASE_KEY, table_key)




def fetch_all_records(table: Table):
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


def search_record_by_id(table: Table, record_id: str):
    """
    Search for a record by ID in a specified table. If not found in the specified table,
    check other available tables.

    Args:
        table (Table): The table to search.
        record_id (str or list): The record ID(s) to search for.

    Returns:
        dict or list: The record(s) found or None if not found in any table or if an error occurred.
    """
    try:
        if isinstance(record_id, list):
            records = [
                CRUD(table, record_id=id, option='read') for id in record_id
            ]
            return records
        elif isinstance(record_id, str):
            # Search in the specified table
            record = CRUD(table, record_id=record_id, option='read')
            if record:
                return record
            else:
                # If not found in the specified table, check other available tables
                available_tables = [company_table, users_table, applications_table]
                for other_table in available_tables:
                    if other_table != table:
                        record = CRUD(other_table, record_id=record_id, option='read')
                        if record:
                            return record
                # If not found in any table, return None
                return None
        else:
            raise ValueError(
                "record_id must be either a string or a list of strings")
    except Exception as e:
        logger.error(f"Error searching for record(s) with ID {record_id}: {e}")
        return None


# TABLES
company_table = init_table(COMPANY_TABLE_KEY)
users_table = init_table(USERS_TABLE_KEY)
applications_table = init_table(APPLICATIONS_TABLE_KEY)

# RECORDS
company_records = fetch_all_records(company_table)
users_records = fetch_all_records(users_table)
applications_records = fetch_all_records(applications_table)
