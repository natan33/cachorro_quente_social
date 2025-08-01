// Importando o JavaScript do Bootstrap (inclui o Popper)

// Continue com suas outras importações
import $ from 'jquery';

import 'bootstrap/dist/css/bootstrap.min.css';  // Certifique-se de que o CSS seja importado
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import Swal from 'sweetalert2';
import { showAlert } from '../components/sweet-geral';

$(document).ready(function () {
    //const salesTable = $('#salesTable').DataTable();

    const form = $('#saleForm');
    const modal = form.closest('.modal');
    const modalId = modal.attr('id');

    const product = {
        id: 1,
        name: "Cachorro Quente",
        price: 5.00
    };

    function updateTotal() {
        let quantity = parseInt($('#quantity').val()) || 1;
        let total = product.price * quantity;
        $('#totalAmount').text(`R$ ${total.toFixed(2)}`);
    }

    $('#quantity').on('input change', updateTotal);

    $('#saleForm').on('submit', function (e) {
        e.preventDefault();

        const quantity = parseInt($('#quantity').val());
        if (quantity <= 0) {
            showAlert({
                icon: 'warning',
                title: 'Quantidade inválida',
                text: 'Quantidade deve ser maior que zero.',
            });
            return;
        }

        const buyerName = $('#buyerName').val().trim();

        if (buyerName && !isNaN(buyerName)) {
            showAlert({
                icon: 'error',
                title: 'Nome inválido',
                text: 'O nome do comprador não pode ser um número.'
            });
            return;
        }

        const paymentMethod = $('#paymentMethod').val();
        // Se quiser validar o método de pagamento, faça aqui. Se não, pode deixar passar.

        const paymentStatus = $('input[name="payment_status"]:checked').val();

        const saleData = {
            items: [
                {
                    product_id: product.id,
                    quantity: quantity
                }
            ],
            buyerName: buyerName,
            payment_method: paymentMethod,
            payment_status: paymentStatus,
            notes: $('#notes').val()
        };

        $.ajax({
            url: "/sell",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(saleData),
            success: function (response) {
                if (response.success) {
                    
                    form[0].reset();

                    // Restante do código para atualizar a tabela
                    $('#salesTable').DataTable().ajax.reload();

                    $('#fechar-modal-add-venda').trigger('click');

                    Swal.fire({ title: "Pedido enviado com sucesso!", icon: "success", timer: 1000, showConfirmButton: false });
                    //(modalId)
                    setTimeout(() => {
                        Swal.close();

                    }, 1600);
                }
            },
            error: function (xhr) {
                const errorMessage = xhr.responseJSON ? xhr.responseJSON.message : 'Erro desconhecido.';
                showAlert({
                    icon: 'error',
                    title: 'Erro ao registrar venda',
                    text: errorMessage,
                });
            }
        });

    });

    updateTotal();
});
