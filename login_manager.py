from flask_login import LoginManager
from app import app
from flask import redirect, request

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    """
    Handle unauthorized access attempts.

    Returns:
        Redirect: Redirects the user to the login page with a 'next' parameter.
    """
    next_url = request.path.strip('/')
    return redirect(f'/login?next={next_url}')
