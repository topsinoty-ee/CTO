from flask_login import current_user
from flask import redirect, render_template, request
from api.airtable_ops import (APPLICATIONS_TABLE_KEY, applications_table,
                              search_record_by_id, fetch_all_records,
                              company_table, COMPANY_TABLE_KEY)
from api.logging_config import logger


# Home page
def home():
    """
    Render the homepage.

    If the user is authenticated, redirect them to their company dashboard.
    Otherwise, render the homepage.

    Returns:
        str: Rendered HTML template for the homepage.
    """

    if current_user.is_authenticated:
        return redirect(f'/{current_user.id}/company-dashboard')
    else:
        return render_template('index.html')


# All applications page
def all_applications():
    """
    Handle GET and POST requests for the job offers page.

    GET:
        Render the job offers page with company records.

    POST:
        Handle form submissions for job offers.

    Returns:
        str: Rendered HTML template for the job offers page.
    """

    applications_data = fetch_all_records(applications_table)
    logger.info(applications_data)

    return render_template('all-applications.html',
                           table=APPLICATIONS_TABLE_KEY,
                           applications_table=applications_table,
                           data=applications_data,
                           search=search_record_by_id)


# All companies page
def all_companies():
    """
    Display all companies with specific fields.

    Returns:
        str: Rendered HTML template for all companies with company records.
    """

    companies_data = fetch_all_records(company_table)

    return render_template('all_companies.html',
                           data=companies_data,
                           search=search_record_by_id)


# User dashboard
def dashboard(company_id):
    """
    Display the company's dashboard.

    Args:
        company_id (str): The ID of the company.

    Returns:
        str: Rendered HTML template for the company's dashboard with company data.
    """

    company_data = search_record_by_id(company_table, company_id)

    return render_template('dashboard.html',
                           company_data=company_data,
                           table=COMPANY_TABLE_KEY)


def company_applications(company_id):
    """
    Display the company's applications page.

    Args:
        company_id (str): The ID of the company.

    Returns:
        str: Rendered HTML template for the company's applications page.
    """
    if request.method == 'POST':
        # Handle form submission logic here, if any
        pass

    company_data = search_record_by_id(company_table, company_id)
    applications_data = []
    all_company_application_ids = company_data['fields'].get(
        'applications', [])

    for application_id in all_company_application_ids:
        application_data = search_record_by_id(applications_table,
                                               application_id)
        applications_data.append(application_data)

    logger.info(applications_data)
    return render_template(
        'applications.html',
        data=applications_data,
        table=APPLICATIONS_TABLE_KEY,
        is_addable=True,  # Adjust as per your requirements
        current_user=current_user.id)
