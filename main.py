from flask import Flask, render_template, request
import os
from api import (
    company_table, company_records, 
    users_table, users_records, 
    applications_table, applications_records, 
    search_record_by_id, fetch_all_records, init_table
)

app = Flask(\
    __name__,
    template_folder='templates',
    static_folder='static'
)

@app.route('/', methods=['GET'])
def home():
    """
    Render the homepage.

    Returns:
        Rendered HTML template for the homepage.
    """
    return render_template('index.html')

@app.route('/job-offers', methods=['GET', 'POST'])
def job_offers():
    """
    Handle GET and POST requests for the job offers page.

    GET:
        Render the job offers page with company records.

    POST:
        Handle form submissions for job offers.

    Returns:
        Rendered HTML template for the job offers page.
    """
    if request.method == 'POST':
        # Handle form submission logic here, if any
        pass
    return render_template(
        'job_offers.html',
        company_records=company_records,
        search=search_record_by_id
    )

@app.route('/all-companies', methods=['GET'])
def all_companies():
    """
    Display all companies with specific fields.

    Returns:
        Rendered HTML template for all companies with company records.
    """
    fields = [
        'Name',
        'ID',
        'Contact',
        'Benefits',
        'Description',
        'Applications',
        'About',
        'Salary',
        'Applicants'
    ]

    # Build the companies_data list using list comprehension
    companies_data = [
        {f'company_{field.lower()}': company['fields'].get(field, '') for field in fields}
        for company in company_records
    ]

    return render_template(
        'all_companies.html',
        company_records=companies_data,
        search=search_record_by_id
    )

@app.route('/new-hires', methods=['GET'])
def new_hires():
    """
    Display the new hires page.

    Returns:
        Rendered HTML template for new hires with company records.
    """
    return render_template('look_hires.html', company_records=company_records)

@app.route('/browse-all', methods=['GET'])
def browse_all():
    """
    Display the browse all page with company records.

    Returns:
        Rendered HTML template for browsing all records with company records.
    """
    return render_template(
        'browse_all.html',
        company_records=company_records, 
        search=search_record_by_id
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
