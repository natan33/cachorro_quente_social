from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for,session
from flask_login import login_required, current_user
from app.models import Sale, Product, User, SaleItem
from app import db, executor, mail
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from app.view.main import main


def get_tipe_pagamento(key=None):
    if key == '1':
        return 'PIX'
    elif key == '2':
        return 'Cartão Crédito'
    elif key == '3':
        return 'Cartão Débito'
    elif key == '4':
        return 'Dinheiro'


@main.route('/')
@main.route('/dashboard')
@login_required
def index():

    session.permanent = True

    from app.view.forms.form_dashborads import SaleForm,EditSaleForm
    register_sale_form = SaleForm(request.form)
    register_sale_form.product_name.data = 'Cachorro Quente'
    form_edite = EditSaleForm(request.form)

    if request.method == 'POST':
        tp_form = request.form.get("tp_form")
        print(f"Tipo de formulário: {tp_form}")

    # Aqui você pode pré-carregar alguns dados para os cards e filtros iniciais
    # Por exemplo, produtos mais vendidos, total de vendas do dia, etc.
    # Vamos focar na integração com DataTables via AJAX para os dados principais.
    return render_template('dashboard.html',register_sale_form=register_sale_form, form_edite=form_edite)

@main.route('/api/sales', methods=['GET'])
@login_required
def get_sales():
    draw = int(request.args.get('draw', 1))
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))
    search_value = request.args.get('search[value]', '')
    order_column_index = request.args.get('order[0][column]', 0, type=int)
    order_direction = request.args.get('order[0][dir]', 'asc')

    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    product_filter = request.args.get('product_filter')
    user_filter = request.args.get('user_filter')
    payment_method = request.args.get('payment_method_filter')
    status = request.args.get('status_filter')

    query = db.session.query(
        Sale.id,
        Sale.sale_date,
        Product.name.label("product_name"),
        SaleItem.quantity,
        SaleItem.unit_price,
        Sale.total_amount,
        Sale.payment_method,
        Sale.payment_status,
        Sale.notes,
        Sale.buyer,
        User.username.label('seller_username')
    ).join(User, User.id == Sale.user_id) \
     .join(SaleItem, SaleItem.sale_id == Sale.id) \
     .join(Product, Product.id == SaleItem.product_id)

    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        query = query.filter(Sale.sale_date >= start_date)
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)
        query = query.filter(Sale.sale_date < end_date)

    if product_filter:
        query = query.filter(Product.name.like(f'%{product_filter}%'))

    if user_filter:
        query = query.filter(User.username.like(f'%{user_filter}%'))

    if search_value:
        query = query.filter(
            (Sale.payment_method.like(f'%{search_value}%')) |
            (User.username.like(f'%{search_value}%')) |
            (Product.name.like(f'%{search_value}%'))
        )

    if payment_method:
        tipo_pag = get_tipe_pagamento(payment_method)
        query = query.filter(Sale.payment_method == tipo_pag)

    if status:
        if status == '1':
            # Vendas do Dia — você pode filtrar pela data (exemplo: hoje)
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)
            query = query.filter(Sale.sale_date >= today_start, Sale.sale_date < today_end)
        elif status == '2':
            # Total de Vendas (Geral) — pode não filtrar nada (mostrar tudo)
            pass
        elif status == '3':
            # Transações Hoje — similar ao 1, filtrar só as vendas do dia
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)
            query = query.filter(Sale.sale_date >= today_start, Sale.sale_date < today_end)
        elif status == '4':
            # Vendas Pagas
            query = query.filter(Sale.payment_status == 'paid')
        elif status == '5':
            # Vendas Pendentes
            query = query.filter(Sale.payment_status == 'not_paid')
        elif status == '6':
            # Valor a Receber — pode filtrar pagamentos pendentes ou algo mais específico
            query = query.filter(Sale.payment_status == 'not_paid')


    total_records = query.count()

    columns_map = {
        0: Sale.id,
        1: Sale.sale_date,
        2: Product.name,
        3: SaleItem.quantity,
        4: SaleItem.unit_price,
        5: Sale.total_amount,
        6: Sale.payment_method,
        7: Sale.payment_status,
        8: Sale.notes,
        9: Sale.buyer,
        10: User.username
    }
    order_column = columns_map.get(order_column_index, Sale.id)
   

    if order_direction == 'desc':
        query = query.order_by(order_column.desc())
    else:
        query = query.order_by(order_column.asc())

    filtered_records = query.count()
    sales = query.offset(start).limit(length).all()

    data = []
    for sale in sales:
        data.append([
            sale.id,
            sale.sale_date.strftime('%d/%m/%Y %H:%M:%S'),
            sale.product_name,
            sale.quantity,
            f'R$ {sale.unit_price:.2f}',
            f'R$ {sale.total_amount:.2f}',
            sale.payment_method,
            'Pago' if sale.payment_status == 'paid' else 'Pendente',
            sale.notes or '',
            sale.buyer or '',
            sale.seller_username,
            f'''
            <div class="btn-group" role="group">
                <button class="btn btn-sm btn-info view-details" data-id="{sale.id}" title="Detalhes">
                    <i class="bi bi-info-circle"></i>
                </button>
                <button class="btn btn-sm btn-warning edit-sale" data-id="{sale.id}" title="Editar">
                    <i class="bi bi-pencil-square"></i>
                </button>
                <button class="btn btn-sm btn-danger delete-sale" data-id="{sale.id}" title="Excluir">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
            '''.strip()
        ])

    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": data
    })


@main.route('/api/sale_details/<int:sale_id>', methods=['GET'])
@login_required
def get_sale_details(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    items = []
    for item in sale.items:
        items.append({
            'product_name': item.product.name,
            'quantity': item.quantity,
            'unit_price': f'R$ {item.unit_price:.2f}',
            'item_total': f'R$ {item.item_total:.2f}'
        })
    sale_data = {
        'id': sale.id,
        'seller': sale.seller.username,
        'total_amount': f'R$ {sale.total_amount:.2f}',
        'sale_date': sale.sale_date.strftime('%d/%m/%Y %H:%M:%S'),
        'payment_method': sale.payment_method,
        'notes': sale.notes or 'Nenhuma',
        'items': items
    }
    return jsonify(sale_data)




@main.route('/api/dashboard_cards_data', methods=['GET'])
@login_required
def get_dashboard_cards_data():
    today = datetime.now().date()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())

    # Vendas do dia
    daily_sales = db.session.query(func.sum(Sale.total_amount)).filter(
        Sale.sale_date >= start_of_day,
        Sale.sale_date <= end_of_day
    ).scalar() or 0.00

    # Total de vendas (geral)
    total_sales = db.session.query(func.sum(Sale.total_amount)).scalar() or 0.00

    # Quantidade de vendas (transações) do dia
    daily_transactions = db.session.query(Sale.id).filter(
        Sale.sale_date >= start_of_day,
        Sale.sale_date <= end_of_day
    ).count()

    # Top 3 Produtos Mais Vendidos (hoje)
    top_products_today = db.session.query(
        Product.name,
        func.sum(SaleItem.quantity).label('total_quantity')
    ).join(SaleItem, Product.id == SaleItem.product_id)\
     .join(Sale, SaleItem.sale_id == Sale.id)\
     .filter(Sale.sale_date >= start_of_day, Sale.sale_date <= end_of_day)\
     .group_by(Product.name)\
     .order_by(func.sum(SaleItem.quantity).desc())\
     .limit(3).all()

    # Vendas pagas e pendentes
    paid_count = db.session.query(Sale).filter(Sale.payment_status == 'paid').count()
    pending_count = db.session.query(Sale).filter(Sale.payment_status == 'not_paid').count()
    total_pendente_sales = db.session.query(func.sum(Sale.total_amount)).filter(Sale.payment_status == 'not_paid').scalar() or 0.00

    

    top_products_data = [{'name': p.name, 'quantity': p.total_quantity} for p in top_products_today]

    return jsonify({
        'daily_sales': f'R$ {daily_sales:.2f}',
        'total_sales': f'R$ {total_sales:.2f}',
        'daily_transactions': daily_transactions,
        'top_products_today': top_products_data,
        'paid_count': paid_count,
        'pending_count':pending_count,
        'total_pendente_sales': f'R$ {total_pendente_sales:.2f}'
    })

@main.route('/sell', methods=['POST'])
@login_required
def sell():
    sale_data = request.get_json()
    
    if not sale_data:
        return jsonify({'success': False, 'message': 'Dados da venda inválidos'}), 400

    items_data = sale_data.get('items')
    payment_method = sale_data.get('payment_method')
    payment_status = sale_data.get('payment_status', 'not_paid')  # padrão 'not_paid' se não enviado
    notes = sale_data.get('notes')
    buyer = sale_data.get('buyerName')  # Nome do comprador, opcional
    print("Vai salvar com comprador:", buyer)


    if not items_data:
        return jsonify({'success': False, 'message': 'Nenhum item na venda.'}), 400

    total_sale_amount = 0
    sale_items = []
    for item in items_data:
        product_id = item.get('product_id')
        quantity = item.get('quantity')
        product = Product.query.get(product_id)
        if not product or quantity <= 0:
            return jsonify({'success': False, 'message': f'Produto inválido ou quantidade para o produto ID {product_id}.'}), 400

        item_total = product.price * quantity
        total_sale_amount += item_total
        sale_items.append(SaleItem(
            product_id=product.id,
            quantity=quantity,
            unit_price=product.price,
            item_total=item_total
        ))

    try:
        new_sale = Sale(
            user_id=current_user.id,
            total_amount=total_sale_amount,
            payment_method=payment_method,
            payment_status=payment_status,  # <-- adiciona aqui na model
            notes=notes,
            buyer=buyer
        )
        db.session.add(new_sale)
        db.session.flush()  # Para obter o ID da venda antes do commit

        for item in sale_items:
            item.sale_id = new_sale.id
            db.session.add(item)
        db.session.commit()
        print(f"Venda registrada com sucesso: {new_sale.id}")
        

        # Enviar e-mail em segundo plano (se usar executor)
        #executor.submit(send_sale_confirmation_email, new_sale.id, current_user.email, current_user.username)

        return jsonify({'success': True, 'message': 'Venda registrada com sucesso!', 'sale_id': new_sale.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Erro ao registrar venda: {str(e)}'}), 500


# Função para enviar email
def send_sale_confirmation_email(sale_id, recipient_email, username):
    from flask_mail import Message
    try:
        msg = Message(
            f'Confirmação de Venda #{sale_id} - Congresso de Jovens',
            sender='noreply@yourdomain.com', # Deve ser o mesmo do MAIL_DEFAULT_SENDER em config.py
            recipients=[recipient_email]
        )
        msg.body = f"""Olá {username},

Sua venda #{sale_id} foi registrada com sucesso!
Obrigado por ajudar no gerenciamento das vendas de cachorro-quente.

Atenciosamente,
Equipe do Congresso de Jovens
"""
        msg.html = f"""<p>Olá <b>{username}</b>,</p>
<p>Sua venda <b>#{sale_id}</b> foi registrada com sucesso!</p>
<p>Obrigado por ajudar no gerenciamento das vendas de cachorro-quente.</p>
<p>Atenciosamente,<br>
Equipe do Congresso de Jovens</p>
"""
        mail.send(msg)
        print(f"Email de confirmação de venda #{sale_id} enviado para {recipient_email}")
    except Exception as e:
        print(f"Erro ao enviar email para {recipient_email}: {e}")


@main.route('/api/sales/<int:sale_id>', methods=['DELETE'])
@login_required
def delete_sale(sale_id):
    """Exclui uma venda pelo ID."""
    sale = db.session.get(Sale, sale_id)
    if not sale:
        return jsonify({'success': False, 'message': 'Venda não encontrada'}), 404
    
    db.session.delete(sale)
    db.session.commit()
    return jsonify({'success': True})
