// =====================
// Importação de CSS
// =====================
import './main.css';


// =====================
// jQuery e Plugins
// =====================
import $ from 'jquery';
import DataTable from 'datatables.net';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';


// =====================
// Bootstrap JS (inclui Popper e dropdown, modal, etc)
// =====================
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // Bootstrap 5, já inclui Popper.js


import * as bootstrap from 'bootstrap';

// Expõe globalmente
window.$ = $;
window.jQuery = $;
window.bootstrap = bootstrap;
// =====================
// Inicializar plugins
// =====================
$(document).ready(function () {
  // Inicialização DataTables (exemplo, ajuste o seletor da sua tabela)
  // $('#minhaTabela').DataTable();
});

// =====================
// Debug
// =====================
console.log('Vite está funcionando com Flask + Bootstrap!');
