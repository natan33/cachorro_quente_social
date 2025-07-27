from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_executor import Executor
from flask_migrate import Migrate
from flask_assets import Environment

from app.assets import assets

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
executor = Executor()
migrate = Migrate()
#assets = Environment()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    executor.init_app(app)
    migrate.init_app(app, db)
    assets.init_app(app)

    # Configuração do Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    with app.app_context():
        # Importar e registrar blueprints
        from app.view.auth import auth
        from app.view.main import main
        
        app.register_blueprint(auth)
        app.register_blueprint(main)

        # Configurar Flask-Assets (Bundles)
        #from app.assets import compile_static_assets
        #compile_static_assets(assets)

        return app