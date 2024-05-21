from logging import debug
from flask import Flask, render_template, request, redirect
import os
from api import (company_table, company_records, users_table, users_records,
                 applications_table, applications_records, search_record_by_id,
                 fetch_all_records, init_table, sign_up_as_company,
                 login_as_company)
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin

app = Flask(__name__, template_folder='templates', static_folder='static')

app.secret_key = os.urandom(24)

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
        @login_required
        # Handle form submission logic here, if any
        def post_application():
            pass
    return render_template('job_offers.html',
                           company_records=company_records,
                           search=search_record_by_id)


@app.route('/all-companies', methods=['GET'])
def all_companies():
    """
    Display all companies with specific fields.

    Returns:
        Rendered HTML template for all companies with company records.
    """
    fields = [
        'name', 'id', 'contact', 'benefits', 'description', 'applications',
        'about', 'salary', 'applicants'
    ]

    # Build the companies_data list using list comprehension
    companies_data = [{
        f'company_{field.lower()}':
        company['fields'].get(field, '')
        for field in fields
    } for company in company_records]

    return render_template('all_companies.html',
                           company_records=companies_data,
                           search=search_record_by_id)


@app.route('/new-hires', methods=['GET'])
@login_required
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
    return render_template('browse_all.html',
                           company_records=company_records,
                           search=search_record_by_id)


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        company_name = request.form['company_name']

        if not email.strip() and not password.strip(
        ) and not company_name.strip():
            return render_template('sign_up.html',
                                   error='Please fill in all fields.')
        # Sign up as a company
        company = sign_up_as_company(email, password, company_name)

        if company:
            # Redirect to the company's dashboard
            return redirect(f'/company-dashboard/{company["id"]}')
        else:
            # Handle sign-up failure
            return "Sign up failed"
    return render_template('sign_up.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email.strip() and not password.strip():
            return render_template('login.html',
                                   error='Please fill in all fields.')

        # Log in as a company
        company = login_as_company(email, password)
        if company:
            # Redirect to the company's dashboard
            return redirect(f'/company-dashboard/{company["id"]}')
    return render_template('login.html')


@app.route('/company-dashboard/<company_id>', methods=['GET'])
@login_required
def company_dashboard(company_id):
    return render_template('dashboard.html', company_id=company_id)


@app.route('/company-dashboard/<company_id>/applications', methods=['GET'])
@login_required
def company_applications(company_id):
    return render_template('applications.html', company_id=company_id)


if __name__ == "__main__":
    debug=True
    app.run(host='0.0.0.0', port=3000)
    