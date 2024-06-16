import os

API_KEY = os.environ.get('AIRTABLE_API_KEY')
BASE_KEY = os.environ.get('VERIC_BASE_KEY')
COMPANY_TABLE_KEY = os.environ.get('COMPANY_TABLE_KEY')
USERS_TABLE_KEY = os.environ.get('USERS_TABLE_KEY')
APPLICATIONS_TABLE_KEY = os.environ.get('APPLICATIONS_TABLE_KEY')
DROPBOX_ACCESS_TOKEN = os.environ.get('DROPBOX_ACCESS_TOKEN')
DROPBOX_REFRESH_TOKEN = os.environ.get('DROPBOX_REFRESH_TOKEN')
DROPBOX_APP_KEY = os.environ.get('DROPBOX_APP_KEY')
DROPBOX_APP_SECRET = os.environ.get('DROPBOX_APP_SECRET')

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
        'APPLICATIONS_TABLE_KEY': APPLICATIONS_TABLE_KEY,
        'DROPBOX_ACCESS_TOKEN': DROPBOX_ACCESS_TOKEN,
        'DROPBOX_REFRESH_TOKEN': DROPBOX_REFRESH_TOKEN,
        'DROPBOX_APP_KEY': DROPBOX_APP_KEY,
        'DROPBOX_APP_SECRET': DROPBOX_APP_SECRET
    }

    missing_vars = [key for key, value in required_vars.items() if not value]
    if missing_vars:
        raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

check_env_vars()
