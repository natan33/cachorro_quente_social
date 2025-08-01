$(document).ready(function () {
    var salesTable;

    // Função para carregar os dados dos cards
    function loadDashboardCards() {
        $.ajax({
            url: "/api/dashboard_cards_data",
            method: "GET",
            success: function (response) {
                $('#dailySalesCard').text(response.daily_sales);
                $('#totalSalesCard').text(response.total_sales);
                $('#dailyTransactionsCard').text(response.daily_transactions);

                // Atualizar Top Produtos
                var topProductsHtml = '';
                if (response.top_products_today.length > 0) {
                    topProductsHtml += '<h6>Top 3 Produtos Vendidos Hoje:</h6><ul>';
                    $.each(response.top_products_today, function (index, product) {
                        topProductsHtml += '<li>' + product.name + ' (' + product.quantity + ' unidades)</li>';
                    });
                    topProductsHtml += '</ul>';
                } else {
                    topProductsHtml += '<p>Nenhum produto vendido hoje.</p>';
                }
                // Adicione um card ou seção para exibir topProductsHtml no seu dashboard.html
                // Por simplicidade, vou logar aqui para que você veja o formato.
                console.log("Top Produtos Hoje:", topProductsHtml);
            },
            error: function (xhr, status, error) {
                console.error("Erro ao carregar dados dos cards:", error);
            }
        });
    }

    // Inicializa o DataTables
    function initializeDataTable() {
        if ($.fn.DataTable.isDataTable('#salesTable')) {
            $('#salesTable').DataTable().destroy(); // Destrói a instância existente se houver
        }

        salesTable = $('#salesTable').DataTable({
            "processing": true,
            "serverSide": true,
            "ajax": {
                "url": "/api/sales",
                "type": "GET",
                "data": function (d) {
                    d.start_date = $('#startDate').val();
                    d.end_date = $('#endDate').val();
                    d.product_filter = $('#productFilter').val();
                    d.user_filter = $('#userFilter').val();
                }
            },
            "columns": [
                { "data": 0 }, // ID da Venda
                { "data": 1 }, // Data da Venda
                { "data": 2 }, // Valor Total
                { "data": 3 }, // Método Pagamento
                { "data": 4 }, // Vendedor
                { "data": 5, "orderable": false } // Ações (botão Detalhes)
            ],
            "language": {
                "url": "https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json"
            }
            ,
            "order": [[1, "desc"]] // Ordena por Data da Venda (coluna 1) descendente por padrão
        });
    }

    // Carrega dados iniciais dos cards
    loadDashboardCards();
    initializeDataTable();

    // Evento para aplicar filtros
    $('#applyFilters').on('click', function () {
        salesTable.ajax.reload(); // Recarrega os dados da tabela com os novos filtros
        loadDashboardCards(); // Recarrega os cards também, se eles forem impactados pelos filtros de data
    });

    // Evento para limpar filtros
    $('#clearFilters').on('click', function () {
        $('#startDate').val('');
        $('#endDate').val('');
        $('#productFilter').val('');
        $('#userFilter').val('');
        salesTable.ajax.reload();
        loadDashboardCards();
    });

    // Abrir modal de detalhes da venda
    $('#salesTable tbody').on('click', '.view-details', function () {
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
});