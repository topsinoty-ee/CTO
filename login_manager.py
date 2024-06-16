from flask_login import LoginManager


login_manager = LoginManager()
login_manager.init_app(app)