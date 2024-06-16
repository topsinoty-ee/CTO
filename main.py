from flask import Flask, render_template, request, redirect, flash
import os
from flask.helpers import url_for
from api.utils import convert_to_json, CRUD
from api.logging_config import logger
from api.airtable_ops import (company_records, company_table,
                              applications_table, init_table,
                              search_record_by_id)
from api.auth import sign_up_as_company, login_as_company
from api.env_config import APPLICATIONS_TABLE_KEY, COMPANY_TABLE_KEY
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.urandom(24)

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


@login_manager.unauthorized_handler
def unauthorized():
    """
    Handle unauthorized access attempts.

    Returns:
        Redirect: Redirects the user to the login page with a 'next' parameter.
    """
    return redirect(url_for('login', next=request.path.strip('/')))


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
        return render_template('update_form.html',
                               formdata=displayed_data,
                               data=record,
                               table=table)

    return render_template('update_form.html',
                           formdata=displayed_data,
                           is_edit=True)


@app.route('/update/<table_key>/<id>', methods=['POST'])
@login_required
def update_record(table_key: str, id):
    try:
        Table = init_table(table_key)
        record = search_record_by_id(Table, id)
        logger.info(record)
        # write logic that compare
        data = {
            key: value
            for key, value in request.form.items() if value.strip() != ""
        }
        data.pop('id', None)
        files = request.files.to_dict()

        logger.info(f"data: {data}")
        logger.info(f"files: {files}")

        CRUD(Table, record_id=id, data=data, files=files, option='update')
        return redirect(f'/company-dashboard/{current_user.id}')
    except Exception as e:
        logger.error(
            f"Error updating record with ID {id} in table {table_key}: {e}")
        return "An error occurred", 500


@app.route('/add/<table>', methods=['GET', 'POST'])
@login_required
def add_record(table: str):
    displayed_data = []

    if request.method == 'POST':
        form_data = request.form['form_data']
        computed_field = request.form['computed_field']

        if form_data is not None:
            logger.info(f"form_data: {form_data}")
            displayed_data = convert_to_json(form_data)
            displayed_data = [
                field for field in displayed_data if field['editable']
            ]

            logger.info(f"Data to add: {displayed_data}")
            return render_template('add_form.html',
                                   formdata=displayed_data,
                                   table=table,
                                   computed_field=computed_field)

    return render_template('add_form.html',
                           formdata=displayed_data,
                           table=table)


@app.route('/create/<table>', methods=['POST'])
@login_required
def create_record(table: str):
    try:
        Table = init_table(table)

        # Get form data and log it
        formdata = request.form.items()
        computed_field = request.form.get('computed_field')
        logger.info(f"computed_field: {computed_field}")
        logger.info(f"formdata: {formdata}")

        # Parse the computed_field JSON string into a Python dictionary
        computed_field_data = convert_to_json(computed_field)
        logger.info(f"computed_field_data: {computed_field_data}")

        # Add form data to the data dictionary, excluding the computed field initially
        data = {
            key: value
            for key, value in formdata if key != 'computed_field'
        }
        logger.info(f"data: {data}")
        # Add the computed field to the data dictionary
        if 'key' in computed_field_data and 'value' in computed_field_data:
            data[computed_field_data['key']] = [computed_field_data['value']]
        logger.info(f"data after adding computed_field: {data}")

        # Get files and log them
        files = request.files.to_dict()
        logger.info(f'files: {files}')

        # Use CRUD function to create the record
        CRUD(Table, data=data, files=files, option='create')

        # Redirect to the company dashboard
        return redirect(f'/company-dashboard/{current_user.id}')

    except Exception as e:
        logger.error(f"Error adding record to table {table}: {e}")
        return "An error occurred", 500


@app.route('/delete/<table>/<item_id>', methods=['POST'])
@login_required
def delete_item(table, item_id):
    """
    Delete an item from the specified table.

    Args:
        table (str): The table from which to delete the item.
        item_id (str): The ID of the item to delete.

    Returns:
        str: Redirect to the applications page after deletion.
    """
    Table = init_table(table)
    CRUD(Table, item_id, option='delete')
    flash('Item deleted successfully', 'success')
    return redirect(url_for('company_applications',
                            company_id=current_user.id))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
