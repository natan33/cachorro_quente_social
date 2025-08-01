# app/__init__.py
import os
from flask import Flask, url_for, g ,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_executor import Executor
from flask_migrate import Migrate
from flask_compress import Compress
import json

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
executor = Executor()
migrate = Migrate()
compress = Compress()

def create_app():
    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'dist'),
        static_url_path='/static' # O caminho da URL no navegador
    )
    app.config.from_object('app.config.Config')

    app.config['COMPRESS_MIMETYPES'] = ['text/html', 
        'text/css','text/xml' ,'application/javascript', 'application/json']
    app.config['COMPRESS_LEVEL'] = 6
    app.config['COMPRESS_MIN_SIZE'] = 500


    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    executor.init_app(app)
    migrate.init_app(app, db)
    compress.init_app(app)

    # CONFIGURACOES DO FLASK-COMPRESS

    login_manager.login_view = 'auth.login' # ou 'auth.login' se seu blueprint se chama 'auth'
    login_manager.login_message_category = 'info'

    _manifest = {} # Dicionário para armazenar o manifest

    def vite_asset(filename):
        if app.debug or not _manifest:
            manifest_path =fr'/home/natan/cachorro_quente_social-development/app/static/dist/.vite/manifest.json' # VOLTE PARA O CAMINHO DINÂMICO
            if not os.path.exists(manifest_path):
                print(f"ATENÇÃO: manifest.json não encontrado em {manifest_path}. Execute 'npm run build'.")
                print(f"Entradas disponíveis no manifest: {list(_manifest.keys())}")
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


    @app.before_request
    def disable_compreesion_for_static():
        if request.path.startswith('/static/'):
            request.environ['no-compression'] = True

    with app.app_context():
        # Importar e registrar blueprints
        from app.view.auth import auth # Verifique o nome real do seu blueprint
        from app.view.main import main # Verifique o nome real do seu blueprint
        from app.view.api import api # Verifique o nome real do seu blueprint
        
        app.register_blueprint(auth)
        app.register_blueprint(main)
        app.register_blueprint(api)
        # REMOVA ESTAS LINHAS: ELAS SÃO REDUNDANTES OU CONFLITANTES
        # app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        # app.add_url_rule(
        #     '/static/dist/<path:filename>',
        #     endpoint='dist_static',
        #     view_func=app.send_static_file
        # )

        return app