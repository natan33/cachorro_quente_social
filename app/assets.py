# app/assets.py
from flask_assets import Bundle, Environment

# MUITO IMPORTANTE: Crie a instância 'assets' GLOBALMENTE neste arquivo
assets = Environment()

# Agora, registre seus bundles usando esta instância 'assets'
assets.register('main_css', Bundle(
    'bootstrap/dist/css/bootstrap.min.css',
    'datatables.net-dt/css/dataTables.bootstrap5.min.css',
    '../app/static/css/custom.css',
    output='gen/packed.css',
    filters='cssmin'
))

assets.register('main_js', Bundle(
    'jquery/dist/jquery.min.js',
    'bootstrap/dist/js/bootstrap.bundle.min.js',
    'datatables.net/js/jquery.dataTables.min.js',
    'datatables.net-dt/js/dataTables.bootstrap5.min.js',
    '../app/static/js/custom.js',
    output='gen/packed.js',
    filters='jsmin'
))