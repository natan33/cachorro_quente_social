from app import db, login_manager
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())

    sales_items = db.relationship('SaleItem', backref='product', lazy='dynamic')

    def __repr__(self):
        return f'<Product {self.name}>'

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.now())
    payment_method = db.Column(db.String(50)) # Ex: 'Dinheiro', 'Cartão', 'PIX'
    notes = db.Column(db.Text)

    items = db.relationship('SaleItem', backref='sale', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Sale {self.id} - Total: {self.total_amount}>'

class SaleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False) # Preço do produto no momento da venda
    item_total = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f'<SaleItem Sale: {self.sale_id} Product: {self.product_id} Qty: {self.quantity}>'