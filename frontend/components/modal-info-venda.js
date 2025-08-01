import $ from 'jquery';

// saleDetailsModal.js
import * as bootstrap from 'bootstrap';

export function setupSaleDetailsModal() {
    $('#salesTable tbody').on('click', '.view-details', function () {

        // Pega o Id da linha da tabela
        var saleId = $(this).data('id');
        $.ajax({
            url: `/api/sale_details/${saleId}`,
            method: 'GET',
            success: function (response) {
                $('#modalSaleId').text(response.id);
                $('#modalSeller').text(response.seller);
                $('#modalSaleDate').text(response.sale_date);
                $('#modalTotalAmount').text(response.total_amount);
                $('#modalPaymentMethod').text(response.payment_method);
                $('#modalNotes').text(response.notes);

                // gera Uuma linha na tabela de itens da venda
                var itemsHtml = '';
                $.each(response.items, function (index, item) {
                    itemsHtml += `
                        <tr>
                            <td>${item.product_name}</td>
                            <td>${item.quantity}</td>
                            <td>${item.unit_price}</td>
                            <td>${item.item_total}</td>
                        </tr>
                    `;
                });

                $('#modalSaleItems').html(itemsHtml);

                var saleDetailsModal = new bootstrap.Modal(document.getElementById('saleDetailsModal'));
                saleDetailsModal.show();
            },
            error: function (xhr, status, error) {
                alert('Erro ao carregar detalhes da venda: ' + error);
            }
        });
    });
}
