# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_executor import Executor
from flask_migrate import Migrate

# Remova esta linha se existir: from flask_assets import Environment

# Importe a instância 'assets' que você criou em app/assets.py
from app.assets import assets 

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
executor = Executor()
migrate = Migrate()
# Garanta que esta linha esteja comentada ou removida:
# assets = Environment() 

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # --- Configurações do Flask-Assets DEVEM VIR AQUI, ANTES de assets.init_app(app) ---
    app.config['ASSETS_ROOT'] = os.path.join(app.root_path, '..', 'node_modules')
    app.config['ASSETS_URL'] = '/static/gen' # Caminho onde os bundles serão servidos
    app.config['ASSETS_DEBUG'] = False # Força o Flask-Assets a construir os bundles
    app.config['ASSETS_AUTO_BUILD'] = True
    # ------------------------------------------------------------------------------------

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    executor.init_app(app)
    migrate.init_app(app, db)
    # INICIALIZE A INSTÂNCIA 'assets' DO Flask-Assets COM O SEU APP AQUI:
    assets.init_app(app) 

    # Configuração do Flask-Login
    login_manager.login_view = 'auth_bp.login'
    login_manager.login_message_category = 'info'

    with app.app_context():
        # Tente construir os assets.
        # Este try-except é para depuração; em produção, você faria isso separadamente.
        try:
            assets.build() # <-- Esta linha agora deve funcionar
            print("Assets built successfully!")
        except Exception as e:
            # Se ainda der erro, provavelmente é FileNotFoundError porque os caminhos estão errados.
            print(f"ATENÇÃO: Erro ao construir assets: {e}")

        # Importar e registrar blueprints
        # Verifique se os nomes dos blueprints aqui são os que você realmente está usando (ex: auth_bp, dashboard_bp)
        from app.view.auth import auth 
        from app.view.main import main 
        # from app.view.errors import bp as errors_bp # Se tiver o blueprint de erros

        app.register_blueprint(auth)
        app.register_blueprint(main)
        # app.register_blueprint(errors_bp)

        return app