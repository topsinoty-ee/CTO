from flask import Blueprint, redirect
from flask.helpers import url_for
from route.authentication import *
from route.crud import *
from route.page import *
from route.error import error_404, error_500
from flask_login import login_required

routes_bp = Blueprint('routes', __name__)


@routes_bp.route('/', methods=['GET'])
def home_page():
    return home()


@routes_bp.route('/all-applications', methods=['GET', 'POST'])
def all_applications_page():
    return all_applications()


@routes_bp.route('/all-companies', methods=['GET'])
def all_companies_page():
    return all_companies()


# @routes_bp.route('/new-hires', methods=['GET'])
# def new_hires():
#     """
#     Display the new hires page.

#     Returns:
#         str: Rendered HTML template for new hires with company records.
#     """
#     return render_template('look_hires.html', company_records=company_records)

# @routes_bp.route('/browse-all', methods=['GET'])
# def browse_all():
#     """
#     Display the browse all page with company records.

#     Returns:
#         str: Rendered HTML template for browsing all records with company records.
#     """
#     return render_template('browse_all.html',
#                            company_records=company_records,
#                            search=search_record_by_id)


@routes_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    return login()


@routes_bp.route('/sign-up', methods=['GET', 'POST'])
def sign_up_page():
    return sign_up()


@routes_bp.route('/<company_id>/company-dashboard', methods=['GET'])
@login_required
def user_dashboard(company_id):
    return dashboard(company_id=company_id)

@routes_bp.route('/dashboard', methods=['GET'])
def dashboard_page():
    return redirect(url_for('routes.login_page'))


@routes_bp.route('/<company_id>/applications', methods=['GET', 'POST'])
@login_required
def company_applications_page(company_id):
    return company_applications(company_id=company_id)


@routes_bp.route('/logout')
@login_required
def log_out():
    return logout()


@routes_bp.route('/edit/<table>/<id>', methods=['GET', 'POST', 'PATCH'])
@login_required
def edit_table(table, id):
    return edit(table=table, id=id)


@routes_bp.route('/update/<table_key>/<id>', methods=['POST'])
@login_required
def update_record(table_key, id):
    return update(table_key, id)


@routes_bp.route('/add/<table>', methods=['GET', 'POST'])
@login_required
def add_record(table: str):
    return add(table=table)


@routes_bp.route('/create/<table>', methods=['POST'])
@login_required
def create_record(table: str):
    return create(table=table)


@routes_bp.route('/delete/<table>/<item_id>', methods=['POST'])
@login_required
def delete_item(table, item_id):
    return delete(table, item_id)


@routes_bp.errorhandler(404)
def page_not_found(error):
    return error_404(error)


@routes_bp.errorhandler(500)
def internal_server_error(error):
    return error_500(error)