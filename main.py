from flask import Flask, render_template, request, redirect
import os
from logging import debug, getLogger, basicConfig, INFO
from flask.helpers import url_for
from api import (CRUD, company_table, company_records, applications_records,
                 fetch_all_records, init_table, search_record_by_id,
                 sign_up_as_company, login_as_company, COMPANY_TABLE_KEY)
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
import re

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.urandom(24)

basicConfig(level=INFO)
logger = getLogger(__name__)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    """
    User class for Flask-Login integration. Inherits from UserMixin.

    Attributes:
        id (str): User identifier, typically the company ID.
    """

    def __init__(self, user_id):
        self.id = user_id

    @staticmethod
    def get(user):
        """
        Static method to get the user ID.

        Args:
            user (User): User object.

        Returns:
            str: User ID.
        """
        return user.id


@login_manager.user_loader
def load_user(user_id):
    """
    Load the user from the user ID.

    Args:
        user_id (str): The user ID.

    Returns:
        User: User object with the given user ID.
    """
    return User(user_id)


@app.route('/', methods=['GET'])
def home():
    """
    Render the homepage.

    If the user is authenticated, redirect them to their company dashboard.
    Otherwise, render the homepage.

    Returns:
        str: Rendered HTML template for the homepage.
    """
    if current_user.is_authenticated:
        return redirect(f'/company-dashboard/{current_user.id}')
    else:
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
        str: Rendered HTML template for the job offers page.
    """
    if request.method == 'POST':
        # Handle form submission logic here, if any
        pass
    return render_template('job_offers.html',
                           company_records=company_records,
                           search=search_record_by_id)


@app.route('/all-companies', methods=['GET'])
def all_companies():
    """
    Display all companies with specific fields.

    Returns:
        str: Rendered HTML template for all companies with company records.
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
def new_hires():
    """
    Display the new hires page.

    Returns:
        str: Rendered HTML template for new hires with company records.
    """
    return render_template('look_hires.html', company_records=company_records)


@app.route('/browse-all', methods=['GET'])
def browse_all():
    """
    Display the browse all page with company records.

    Returns:
        str: Rendered HTML template for browsing all records with company records.
    """
    return render_template('browse_all.html',
                           company_records=company_records,
                           search=search_record_by_id)


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
    Handle the sign-up process for companies.

    GET:
        Render the sign-up page.

    POST:
        Process the sign-up form submission and create a new company account.

    Returns:
        str: Rendered HTML template for the sign-up page or redirect to the company's dashboard.
    """
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
            company_id = company["id"].strip('{}')  # Remove curly braces
            return redirect(f'/company-dashboard/{company_id}')
        else:
            # Handle sign-up failure
            return "Sign up failed"
    return render_template('sign_up.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle the login process for companies.

    GET:
        Render the login page.

    POST:
        Process the login form submission and authenticate the user.

    Returns:
        str: Rendered HTML template for the login page or redirect to the company's dashboard.
    """
    if request.method == 'POST':
        next_url = request.args.get('next')

        email = request.form['email']
        password = request.form['password']

        if not email.strip() and not password.strip():
            return render_template('login.html',
                                   error='Please fill in all fields.')

        # Log in as a company
        company = login_as_company(email, password)
        if company:
            # Create a user object with the company ID
            user = User(company['id'])

            # Log in the user
            login_user(user)

            # Redirect to the company's dashboard
            company_id = company["id"].strip('{}')  # Remove curly braces
            if next_url:
                return redirect(
                    f'/company-dashboard/{company_id}?next={next_url}')
            else:
                return redirect(f'/company-dashboard/{company_id}')
        else:
            # Handle login failure
            return render_template('login.html',
                                   error='Invalid email or password')
    return render_template('login.html')


@app.route('/company-dashboard/<company_id>', methods=['GET'])
@login_required
def company_dashboard(company_id):
    """
    Display the company's dashboard.

    Args:
        company_id (str): The ID of the company.

    Returns:
        str: Rendered HTML template for the company's dashboard with company data.
    """

    fields = [
        'name', 'id', 'contact', 'benefits', 'description', 'applications',
        'about', 'salary', 'applicants'
    ]
    company_data = search_record_by_id(company_table, company_id)
    return render_template('dashboard.html',
                           company_data=company_data,
                           table=COMPANY_TABLE_KEY)


@app.route('/applications/<company_id>', methods=['GET', 'POST'])
@login_required
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
    company_applications = []
    for record in applications_records:
        if record['fields']['id'] == company_id:
            company_applications.append(record['fields'])

    return render_template('applications.html',
                           applications=company_applications)


@login_manager.unauthorized_handler
def unauthorized():
    """
    Handle unauthorized access attempts.

    Returns:
        Redirect: Redirects the user to the login page with a 'next' parameter.
    """
    return redirect(url_for('login', next=request.endpoint))


@app.route('/logout')
@login_required
def logout():
    """
    Log out the current user.

    Returns:
        Redirect: Redirects the user to the homepage.
    """
    logout_user()
    return redirect('/')


@app.route('/edit/<table>/<id>', methods=['GET', 'POST', 'PATCH'])
@login_required
def edit(table, id):
    displayed_data = []
    record = search_record_by_id(table, id)
    logger.info(record)
    if request.method == 'POST':
        form_data = request.form['form_data']

        if form_data is not None:
            logger.info(f"form_data: {form_data}")
            displayed_data = convert_to_json(form_data)
        # Process the displayed_data as needed
        logger.info(f"Edited data: {displayed_data}")
        return render_template('form.html',
                               formdata=displayed_data,
                               data=record,
                               table=table)

    return render_template('form.html', formdata=displayed_data)


@app.route('/update/<table_key>/<id>', methods=['POST'])
@login_required
def updaterecord(table_key, id):
    try:
        data = request.form.to_dict()

        # Create a list of keys to remove
        keys_to_remove = []
        for key, value in data.items():
            if value == "":
                keys_to_remove.append(key)

        # Remove the keys with empty values
        for key in keys_to_remove:
            del data[key]

        # Remove the 'id' field from the data dictionary
        data.pop('id', None)

        logger.info(data)

        Table = init_table(table_key)
        CRUD(Table, record_id=id, data=data, option='update')
        return redirect(f'/company-dashboard/{current_user.id}')
    except Exception as e:
        logger.error(f"Error updating record with ID {id} in table {table_key}: {e}")
        return "An error occurred", 500



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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
