from flask import redirect, request, render_template
from api.auth import (sign_up_as_company, login_as_company)
from user import User
from flask_login import login_user, logout_user


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
            return "Sign up failed"
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
                return redirect(f'/{next_url}')
            else:
                return redirect(f'/{company_id}/company-dashboard')
        else:
            # Handle login failure
            return render_template('login.html',
                                   error='Invalid email or password')
    return render_template('login.html')


# Logout
def logout():
    """
    Log out the current user.

    Returns:
        Redirect: Redirects the user to the homepage.
    """
    logout_user()
    return redirect('/')
