from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, RadioField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, NumberRange

class SaleForm(FlaskForm):

    tp_form = HiddenField(default="add_sale")
    product_name = StringField('Produto', render_kw={'readonly': True})

    quantity = IntegerField('Quantidade', validators=[
        DataRequired(message='Informe a quantidade'),
        NumberRange(min=1, message='Quantidade mínima é 1')
    ])

    payment_method = SelectField('Método de Pagamento', choices=[
        ('', 'Selecione...'),
        ('Dinheiro', 'Dinheiro'),
        ('Cartão Débito', 'Cartão Débito'),
        ('Cartão Crédito', 'Cartão Crédito'),
        ('PIX', 'PIX')
    ], validators=[DataRequired(message='Escolha o método de pagamento')])

    payment_status = RadioField('Pagamento efetuado?', choices=[
        ('paid', 'Sim'),
        ('not_paid', 'Não')
    ], default='not_paid', validators=[DataRequired()])

    buyer = StringField('Nome do Comprador (Opcional)', render_kw={'placeholder': 'Digite o nome do comprador'})

    notes = TextAreaField('Observações (Opcional)')

    submit = SubmitField('Finalizar Venda')

    # def preenche_choices(self):
    #     """
    #     Preenche os campos `choices` dos campos do formulário.
    #     """
    #     # Cria a lista de escolhas, adicionando uma tupla para cada analista ordenado
    #     pass
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        #self.preenche_choices()
 
 
    def reset(self):
        """
        usa a variável self para referenciar a instância da classe e definir os campos como None.
        """
        for field in self:
                field.data = None



class EditSaleForm(FlaskForm):
    product_name = StringField('Produto', render_kw={'readonly': True})
 
    buyer = StringField('Nome do Comprador (Opcional)', render_kw={'placeholder': 'Digite o nome do comprador'})
    
    quantity = IntegerField('Quantidade', validators=[
        DataRequired(message='Informe a quantidade'),
        NumberRange(min=1, message='A quantidade mínima é 1')
    ])

    payment_method = SelectField('Método de Pagamento', choices=[
        ('4', 'Dinheiro'),
        ('3', 'Cartão Débito'),
        ('2', 'Cartão Crédito'),
        ('1', 'PIX')
    ], validators=[DataRequired(message='Escolha um método de pagamento')])

    payment_status = RadioField('Status do Pagamento', choices=[
        ('paid', 'Pago'),
        ('not_paid', 'Pendente')
    ], validators=[DataRequired()])

    notes = TextAreaField('Observações')

    submit = SubmitField('Salvar Alterações')
    

    # def preenche_choices(self):
    #     """
    #     Preenche os campos `choices` dos campos do formulário.
    #     """
    #     # Cria a lista de escolhas, adicionando uma tupla para cada analista ordenado
    #    pass
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        #self.preenche_choices()
 
 
    def reset(self):
        """
        usa a variável self para referenciar a instância da classe e definir os campos como None.
        """
        for field in self:
                field.data = None