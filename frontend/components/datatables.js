import $ from 'jquery';
import 'bootstrap-icons/font/bootstrap-icons.css';

let statusFilter = ''; // filtro global para o status

export function initializeDataTable() {
    $.fn.dataTable.ext.errMode = 'throw';

    if ($.fn.DataTable.isDataTable('#salesTable')) {
        $('#salesTable').DataTable().destroy();
    }

    $("#salesTable tbody").css("font-size", "12px");

    const table = $('#salesTable').DataTable({
        dom:
            "<'row'<'col-sm-12 col-md-6 mt-2'l>>" +
            "<'row'<'col-sm-12'B>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        buttons: [
            { extend: "selectAll", text: "Selecionar tudo", className: "btn-select-all" },
            { extend: "selectNone", text: "Limpar seleção", className: "btn-select-none" },
            { extend: "copy", text: "Copiar" },
            "excel",
            { extend: "colvis", text: "Mostrar colunas" },
        ],
        select: {
            style: "multi",
            selector: "td:first-child",
        },
        language: {
            processing: "Carregando...",
            search: "Procurar:",
            lengthMenu: "Mostrar _MENU_ entradas",
            infoFiltered: "(filtrado de um total de _MAX_ registros)",
            info: "Mostrando _START_ a _END_ de _TOTAL_ entradas",
            oPaginate: {
                sNext: "Próximo",
                sPrevious: "Anterior",
            },
        },
        processing: true,
        serverSide: true,
        ajax: {
            url: "/api/sales",
            type: "GET",
            data: function (d) {
                d.start_date = $('#startDate').val();
                d.end_date = $('#endDate').val();
                d.product_filter = $('#productFilter').val();
                d.user_filter = $('#userFilter').val();
                d.payment_method_filter = $('#paymentMethodFilter').val();
                d.status_filter = statusFilter; // usa a variável global aqui
            },
            error: function (xhr, error, code) {
                console.error("Erro ao carregar dados:", xhr.responseText);
            }
        },
        columns: [
            { data: 0 },
            { data: 1 },
            { data: 2 },
            { data: 3 },
            { data: 4 },
            { data: 5 },
            { data: 6 },
            { data: 7 },
            { data: 8 },
            { data: 9 },
            { data: 10 },
            {
                data: 11,
                orderable: false,
                searchable: false,
                className: "text-center"
            }
        ],

        columnDefs: [
            {
                targets: 7,
                render: function (data, type, row) {
                    if (type === 'display') {
                        const badgeClass = data === 'Pago' ? 'bg-success' : 'bg-danger';
                        return `<span class="badge ${badgeClass}">${data}</span>`;
                    }
                    return data;
                }
            }
        ],

        order: [[1, "desc"]],
        fixedHeader: true,
    });

    // Configura clique nos cards para alterar o filtro e recarregar tabela
    function setupCardClickHandlers(table) {
        $('.card').on('click', function () {
            statusFilter = $(this).data('status-filter') || '';
            table.ajax.reload();
        });
    }

    setupCardClickHandlers(table);

    return table;
}
