from flask import Flask, render_template, request, redirect
import os

from flask.helpers import url_for
from api import (company_table, company_records, users_table, users_records,
                 applications_table, applications_records, search_record_by_id,
                 fetch_all_records, init_table, sign_up_as_company,
                 login_as_company)
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):

    def __init__(self, user_id):
        self.id = user_id

    @staticmethod
    def get(user):
        return user.id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/', methods=['GET'])
def home():
    """
    Render the homepage.

    Returns:
        Rendered HTML template for the homepage.
    """
    if current_user.is_authenticated:
        return redirect('/company-dashboard/<company_id>')
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
        Rendered HTML template for the job offers page.
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
            company_id = company["id"].strip('{}')  # Remove curly braces
            return redirect(f'/company-dashboard/{company_id}')
        else:
            # Handle sign-up failure
            return "Sign up failed"
    return render_template('sign_up.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
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
                return redirect(f'/company-dashboard/{company_id}?next={next_url}')
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
    fields = [
        'name', 'id', 'contact', 'benefits', 'description', 'applications',
        'about', 'salary', 'applicants'
    ]
    company_data = search_record_by_id(company_table, company_id)
    return render_template('dashboard.html', company_data=company_data)


@app.route('/company-dashboard/<company_id>/applications', methods=['GET'])
@login_required
def company_applications(company_id):
    return render_template('applications.html', company_id=company_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login', next=request.endpoint))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
