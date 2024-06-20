from flask import Flask
from route.mapping.routes import routes_bp
import os


app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.urandom(24)
app.register_blueprint(routes_bp)