from flask_assets import Bundle

def compile_static_assets(assets):
    # CSS
    assets.register('main_css', Bundle(
        'css/bootstrap.min.css',
        'css/jquery.dataTables.min.css',
        'css/custom.css', # Seu CSS customizado
        output='gen/packed.css',
        filters='cssmin'
    ))

    # JavaScript
    assets.register('main_js', Bundle(
        'js/jquery-3.7.1.min.js', # jQuery baixado localmente
        'js/bootstrap.bundle.min.js',
        'js/jquery.dataTables.min.js',
        'js/custom.js', # Seu JS customizado
        output='gen/packed.js',
        filters='jsmin'
    ))