from app import create_app, db
from flask_migrate import Migrate
from app.models import User, Product, Sale, SaleItem # Importar para que o Flask-Migrate os reconheça

app = create_app()

# Para o Flask-Shell (opcional, para testar modelos)
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Product': Product, 'Sale': Sale, 'SaleItem': SaleItem}

if __name__ == '__main__':
    app.run(debug=True) # Mude para False em produção