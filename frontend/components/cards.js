import $ from 'jquery';

// Função para carregar os dados dos cards
export function loadDashboardCards() {
    $.ajax({
        url: "/api/dashboard_cards_data",
        method: "GET",
        success: function (response) {
            $('#dailySalesCard').text(response.daily_sales);
            $('#totalSalesCard').text(response.total_sales);
            $('#dailyTransactionsCard').text(response.daily_transactions);
            $('#paidSalesCard').text(response.paid_count + ' pagas');
            $('#pendingSalesCard').text(response.pending_count + ' pendentes');
            $('#receivableAmountCard').text(response.total_pendente_sales );

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

export function FilterCards () {
  $('.card').on('click', function() {
    const filter = $(this).data('filter');
    
    $.ajax({
      url: '/api/filter_data',  // rota Flask
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ filter: filter }),
      success: function(response) {
        // Atualiza DataTables com os dados do response
        const table = $('#myDataTable').DataTable();
        table.clear();
        table.rows.add(response.data);  // response.data é um array de objetos
        table.draw();
      },
      error: function() {
        alert('Erro ao carregar dados');
      }
    });
  });
}