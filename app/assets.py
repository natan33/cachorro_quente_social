# app/assets.py
from flask_assets import Bundle, Environment

# Crie a instância do Environment aqui mesmo
# Ela será importada e inicializada em app/__init__.py
assets = Environment()

# Defina seus bundles diretamente usando a instância 'assets'
# A instância `assets` que você criou em `app/__init__.py` será inicializada
# e os bundles serão associados a ela quando você chamar `assets.init_app(app)`
assets.register('main_css', Bundle(
    'css/bootstrap.min.css',
    'css/jquery.dataTables.min.css',
    'css/custom.css', # Seu CSS customizado
    output='gen/packed.css',
    filters='cssmin'
))

assets.register('main_js', Bundle(
    'js/jquery-3.7.1.min.js', # jQuery baixado localmente
    'js/bootstrap.bundle.min.js',
    'js/jquery.dataTables.min.js',
    'js/custom.js', # Seu JS customizado
    output='gen/packed.js',
    filters='jsmin'
))