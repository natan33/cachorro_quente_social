$(document).ready(function () {
    const salesTable = $('#salesTable').DataTable();

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
            alert('Quantidade deve ser maior que zero.');
            return;
        }

        const paymentMethod = $('#paymentMethod').val();
        if (!paymentMethod) {
            alert('Por favor, selecione o método de pagamento.');
            return;
        }

        const paymentStatus = $('input[name="payment_status"]:checked').val();

        const saleData = {
            items: [
                {
                    product_id: product.id,
                    quantity: quantity
                }
            ],
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
                alert(response.message);
                if (response.success) {
                    // reset form
                    $('#quantity').val(1);
                    $('#paymentMethod').val('');
                    $('#notes').val('');
                    $('input[name="payment_status"][value="not_paid"]').prop('checked', true);
                    updateTotal();
                    $('#registerSaleModal').modal('hide');

                    const newRowData = [
                        response.sale_id,
                        new Date().toLocaleString('pt-BR'),
                        `R$ ${(product.price * quantity).toFixed(2)}`,
                        paymentMethod,
                        'SeuUsuario',  // Ajuste para o nome do usuário real
                        '<button class="btn btn-sm btn-info">Detalhes</button>'
                    ];

                    salesTable.row.add(newRowData).draw(false);
                }
            },
            error: function (xhr) {
                const errorMessage = xhr.responseJSON ? xhr.responseJSON.message : 'Erro desconhecido.';
                alert('Erro ao registrar venda: ' + errorMessage);
            }
        });
    });

    updateTotal();
});
