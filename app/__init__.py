# app/__init__.py
import os
from flask import Flask, url_for, g 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_executor import Executor
from flask_migrate import Migrate
import json

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
executor = Executor()
migrate = Migrate()

def create_app():
    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'dist'),
        static_url_path='/static' # O caminho da URL no navegador
    )
    app.config.from_object('app.config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    executor.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login' # ou 'auth.login' se seu blueprint se chama 'auth'
    login_manager.login_message_category = 'info'

    _manifest = {} # Dicionário para armazenar o manifest

    def vite_asset(filename):
        if app.debug or not _manifest:
            manifest_path =fr'C:\Users\natan\Área de Trabalho\cachorro_quente\app\static\dist\manifest.json' # VOLTE PARA O CAMINHO DINÂMICO
            if not os.path.exists(manifest_path):
                print(f"ATENÇÃO: manifest.json não encontrado em {manifest_path}. Execute 'npm run build'.")
                return url_for('static', filename=filename) 
            with open(manifest_path, 'r', encoding='utf-8') as f:
                _manifest.clear()
                _manifest.update(json.load(f))

        entry = _manifest.get(filename)
        if entry:
            return url_for('static', filename=entry['file'])
        else:
            print(f"ATENÇÃO: Entrada '{filename}' não encontrada no manifest.json. Verifique o input no vite.config.js.")
            return url_for('static', filename=filename)

    app.jinja_env.globals['vite_asset'] = vite_asset

    with app.app_context():
        # Importar e registrar blueprints
        from app.view.auth import auth # Verifique o nome real do seu blueprint
        from app.view.main import main # Verifique o nome real do seu blueprint
        
        app.register_blueprint(auth)
        app.register_blueprint(main)

        # REMOVA ESTAS LINHAS: ELAS SÃO REDUNDANTES OU CONFLITANTES
        # app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        # app.add_url_rule(
        #     '/static/dist/<path:filename>',
        #     endpoint='dist_static',
        #     view_func=app.send_static_file
        # )

        return app