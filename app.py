from flask import Flask
from route import routes_bp
from utils.filter import filter_bp
from api.Dropbox import dropbox_ops_bp
from route.error import error_404, error_500
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.urandom(24)
app.register_blueprint(routes_bp)
app.register_blueprint(filter_bp)
app.register_blueprint(dropbox_ops_bp, url_prefix='/dropbox')

@app.errorhandler(404)
def page_not_found_global(error):
    return error_404(error)

@app.errorhandler(500)
def internal_server_error_global(error):
    return error_500(error)