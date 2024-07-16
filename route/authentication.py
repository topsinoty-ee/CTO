from flask import redirect, request, render_template
from api.auth import (sign_up_as_company, login_as_company)
from user import User
from flask_login import login_user, logout_user, current_user
from api.logging_config import logging

logger = logging.getLogger(__name__)


# Sign up
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
            return redirect(f'/{company_id}/company-dashboard')
        else:
            # Handle sign-up failure
            return render_template('sign-up.html', email_taken=True)
    return render_template('sign_up.html')


# Log in
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
    if current_user.is_authenticated:
        return redirect('/')
        
    next_url = request.args.get('next')
    logger.info(request.full_path)
    logger.info(f'Next URL (before POST check): {next_url}')

    if request.method == 'POST':
        logger.info(f'Next URL (after POST check): {next_url}')

        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        next_url = request.form.get('next', '').strip()

        if not email or not password:
            return render_template('login.html', error='Please fill in all fields.')

        # Log in as a company
        company = login_as_company(email, password)
        if company:
            # Create a user object with the company ID
            user = User(company['id'])

            # Log in the user
            login_user(user, remember=True)

            if next_url:
                return redirect(f'/{next_url}')
            else:
                return redirect(f'/{current_user.id}/company-dashboard')
        else:
            # Handle login failure
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html', next_url=next_url)

# Logout
def logout():
    """
    Log out the current user.

    Returns:
        Redirect: Redirects the user to the homepage.
    """
    logout_user()
    return redirect('/')
