import $ from 'jquery';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import Swal from 'sweetalert2';
import Choices from 'choices.js';
import 'choices.js/public/assets/styles/choices.min.css';
import { initializeDataTable } from '../components/datatables.js';
import { loadDashboardCards } from '../components/cards.js';
import { setupSaleDetailsModal } from '../components/modal-info-venda.js';

import { initChoicesAjax } from '../components/select-choice.js';
import { confirmDelete } from '../components/sweet-delete.js';
import { setupEditSaleDetailsModal } from '../components/modal-edit-venda.js'
import { eventFormEditVenda } from '../components/forms-edit-venda.js';
import  { exportToExcel} from '../components/send-email.js';


document.addEventListener('DOMContentLoaded', () => {
  initChoicesAjax('#paymentMethodFilter', '/api/payment_methods');
  initChoicesAjax('#statusFilter', '/api/payment_status');
});


document.addEventListener('click', function (e) {
  const btn = e.target.closest('.delete-sale');
  if (!btn) return;

  const saleId = btn.dataset.id;
  const url = `/api/sales/${saleId}`;

  confirmDelete(url, () => {
    // Reload na tabela após exclusão
    $('#salesTable').DataTable().ajax.reload(null, false);
  });
});


$(document).ready(function () {
    
    // Carrega dados iniciais dos cards
    loadDashboardCards();

    // Inicializa o DataTable
    const salesTable = initializeDataTable();



    
    //initSelect2('productFilter', '/api/products');
    //initSelect2('userFilter', '/api/users');
    //console.log("Inicializando Select2");


    // Evento para aplicar filtros
    $('#applyFilters').on('click', function () {
        salesTable.ajax.reload();
        
        // Recarrega os cards também
        loadDashboardCards();  
    });

    // Limpa os filtros
    $('#clearFilters').on('click', function () {
        $('#startDate').val('');
        $('#endDate').val('');
        $('#productFilter').val('');
        $('#userFilter').val('');
        $('#paymentMethodFilter').val('');
        $('#statusFilter').val('');

        salesTable.ajax.reload();
        loadDashboardCards();
    });

    // Abrir modal de detalhes da venda
    setupSaleDetailsModal();

    // Abrir modal de editar venda
    setupEditSaleDetailsModal();

    // Evento para o formulário de edição de venda
    eventFormEditVenda();


    // Evento para exportar para Excel
    exportToExcel();

});