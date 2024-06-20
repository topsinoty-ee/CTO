from .utils import CRUD
from .airtable_ops import company_table, fetch_all_records
import bcrypt
from .logging_config import logging

logger = logging.getLogger(__name__)


def sign_up_as_company(email: str, password: str, company_name: str):
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
        if not email or not password or not company_name:
            raise ValueError(
                "Email, password, and company name must be provided.")

        # Check if email already exists
        all_emails = [
            company['fields'].get('email')
            for company in fetch_all_records(company_table)
        ]
        if email in all_emails:
            raise ValueError(
                "A company with this email already exists. Please try another email."
            )

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                                        bcrypt.gensalt())
        logger.info(f"Hashed password for {email}")

        # Create the company record
        company_record = CRUD(table=company_table,
                              data={
                                  'email': email,
                                  'password': hashed_password.decode('utf-8'),
                                  'name': company_name
                              },
                              option='create')
        if company_record is not None:
            logger.info(
                f"Created company record with ID: {company_record['id']}")
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
        companies_records = company_table.all(formula=f"{{email}} = '{email}'")
        if not companies_records:
            logger.warning(f"No company found with email: {email }")
            return None
        company = companies_records[0]['fields']
        if bcrypt.checkpw(password.encode('utf-8'),
                          company['password'].encode('utf-8')):
            logger.info(
                f"Company logged in: \"{company['id']}\" with account: \"{email}\""
            )
            return company
        logger.warning(f"Invalid password for company: {email}")
        return None
    except Exception as e:
        logger.error(f"Error logging in \"{email}\": {e}")
        return None
