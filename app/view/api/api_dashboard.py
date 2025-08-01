from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Sale, Product, User, SaleItem
from app import db, executor, mail
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from app.view.api import api

from app.models import *

import os


def get_tipe_pagamento(key=None):
    if key == 'PIX':
        return '1'
    elif key == 'Cartão Crédito':
        return '2'
    elif key == 'Cartão Débito':
        return '3'
    elif key ==  'Dinheiro':
        return '4'


@api.route('/api/products')
@login_required
def get_products():
    produtos = Product.query.all()
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "price": p.price
    } for p in produtos])

@api.route('/api/payment_methods')
@login_required
def opcoes_select():
    term = request.args.get('term', '').lower()
    all_options = [
        { "id": "", "text": "" },
        { "id": "1", "text": "PIX" },
        { "id": "2", "text": "Cartão de Crédito" },
        { "id": "3", "text": "Cartão de Débito" },
        { "id": "4", "text": "Dinheiro" }
    ]

    # Filtra apenas as opções que contenham o termo digitado
    filtered = [opt for opt in all_options if term in opt["text"].lower()]

    return jsonify(filtered)

@api.route('/api/payment_status')
@login_required
def payment_status():
    term = request.args.get('term', '').lower()
    all_options = [
        { "id": "", "text": "" },
        { "id": "1", "text": "Pago" },
        { "id": "2", "text": "Pendente" },
    ]

    # Filtra apenas as opções que contenham o termo digitado
    filtered = [opt for opt in all_options if term in opt["text"].lower()]

    return jsonify(filtered)


@api.route('/api/edit_sale/<int:id_>')
def get_sale_details(id_):
    try:
        def tratar_valor_vazio(valor):
                return valor if valor else None

        

        data = Sale.query.get(id_)

        
        if not data:
            return jsonify({"error": "Item não encontrado"}),404

        data_sale_item = SaleItem.query.filter_by(id = data.id).first()
        print(f'data_sale_item: {data.payment_method}')
        payment_method = get_tipe_pagamento(key=data.payment_method)

        print(f'payment_method: {payment_method}')
        item_data = {
            'id': tratar_valor_vazio(data.id if data else None),
            'payment_method': payment_method,
            'payment_status': tratar_valor_vazio(data.payment_status if data else None),
            'notes': tratar_valor_vazio(data.notes if data else None),
            'buyer': tratar_valor_vazio(data.buyer if data else None ),

            'quantity': tratar_valor_vazio(data_sale_item.quantity if data_sale_item else None),
            'item_total': tratar_valor_vazio(data_sale_item.item_total if data_sale_item else None),
            'total_amount': tratar_valor_vazio(data.total_amount if data else None),
            'unit_price': tratar_valor_vazio(data_sale_item.unit_price if data_sale_item else None),
        }

        return jsonify(item_data)


        
    except Exception as e:
        print('erro na route get_sale_details',e)
        return jsonify({"error": str(e)}),404
    

@api.route('/api/edit_sale', methods=['POST'])
@login_required
def edit_sale():  
    total_sale_amount = 0
    def get_tipe_pagamento(key=None):
        if key == '1':
            return 'PIX'
        elif key == '2':
            return 'Cartão Crédito'
        elif key == '3':
            return 'Cartão Débito'
        elif key == '4':
            return 'Dinheiro'      

    try:
        data = request.form
        print(f'data: {data}')
        sale_id = data.get('id_atual')
        payment_method = data.get('payment_method')
        payment_status = data.get('payment_status')
        notes = data.get('notes')
        buyer = data.get('buyer')
        quantity = int(data.get('quantity') or 1)

        total_amount = 5.00 * quantity  
        total_sale_amount += total_amount

        sale = Sale.query.get(sale_id)
        if not sale:
            return jsonify({"error": "Venda não encontrada"}), 404
        print(f'sale: {sale}')
        sale.payment_method = get_tipe_pagamento(payment_method)
        sale.payment_status = payment_status
        sale.notes = notes
        sale.buyer = buyer
        sale.total_amount = total_sale_amount

        # Atualiza o SaleItem associado
        sale_item = SaleItem.query.filter_by(sale_id=sale_id).first()
        if not sale_item:
            return jsonify({"error": "Item de venda não encontrado"}), 404

        sale_item.quantity = quantity
        sale_item.item_total = total_amount
        sale_item.unit_price = 5.00

        db.session.commit()

        return jsonify({"message": "Venda editada com sucesso!"}), 200

    except Exception as e:
        print(f'Erro ao editar venda: {e}')
        return jsonify({"error": str(e)}), 500






# Configurações do servidor SMTP (exemplo Gmail)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'seuemail@gmail.com'
SMTP_PASSWORD = 'suasenha'

# Caminho do arquivo Excel a ser enviado
EXCEL_FILE_PATH = 'relatorio.xlsx'  # Ajuste o caminho conforme o seu projeto

@api.route('/api/send_excel', methods=['POST'])
def send_excel():
    data = request.get_json()

    # Pega a lista de emails
    emails = data.get('emails', [])
    print(f'Emails recebidos: {emails}')

    if not emails:
        return jsonify({'success': False, 'message': 'Nenhum email fornecido.'}), 400

    # Verifique se o arquivo Excel existe
    #if not os.path.isfile(EXCEL_FILE_PATH):
    #    return jsonify({'success': False, 'message': 'Arquivo Excel não encontrado.'}), 404

    try:
    #     # Lê o conteúdo do arquivo Excel para anexar no email
    #     with open(EXCEL_FILE_PATH, 'rb') as f:
    #         file_data = f.read()
    #         file_name = os.path.basename(EXCEL_FILE_PATH)

    #     # Cria o servidor SMTP e autentica
    #     server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    #     server.starttls()
    #     server.login(SMTP_USER, SMTP_PASSWORD)

    #     for email in emails:
    #         msg = EmailMessage()
    #         msg['Subject'] = 'Relatório Excel'
    #         msg['From'] = SMTP_USER
    #         msg['To'] = email
    #         msg.set_content('Segue em anexo o relatório Excel solicitado.')

    #         # Anexa o arquivo Excel
    #         msg.add_attachment(file_data, maintype='application', subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=file_name)

    #         server.send_message(msg)

    #     server.quit()

        return jsonify({'success': True, 'message': 'E-mails enviados com sucesso.'}),201

    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro ao enviar e-mails: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)

