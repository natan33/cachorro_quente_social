import $ from 'jquery';

// saleDetailsModal.js
import * as bootstrap from 'bootstrap';

export function setupEditSaleDetailsModal() {
    $('#salesTable tbody').on('click', '.edit-sale', function () {

        // Pega o Id da linha da tabela
        var saleId = $(this).data('id');
        $.ajax({
            url: `/api/edit_sale/${saleId}`,
            method: 'GET',
            success: function (response) {
                $('#productNameEdite').val('Cachorro Quente');
                $('#buyerNameEdite').val(response.buyer);
                $('#quantityEdite').val(response.quantity);
                $('#paymentMethodEdite').val(response.payment_method);
                $('#notesEdite').val(response.notes);
                $('#totalAmountIdeti').text(`R$ ${response.total_amount}`);
                
                $(`input[name="payment_status"][value="${response.payment_status}"]`).prop('checked', true);
                // gera Uuma linha na tabela de itens da venda

                var saleDetailsModal = new bootstrap.Modal(document.getElementById('EditeSaleModal'));
                saleDetailsModal.show();
            },
            error: function (xhr, status, error) {
                alert('Erro ao carregar detalhes da venda: ' + error);
            }
        });
    });
}
