// Importe seu CSS principal (que por sua vez importará o CSS das libs)
import './main.css';

// Importe as dependências JavaScript
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // Bootstrap JS com Popper
import $ from 'jquery'; // Importe jQuery e atribua-o à variável $
import DataTable from 'datatables.net'; // Importe DataTables core

// Certifique-se de que jQuery está globalmente acessível para plugins antigos
// e para DataTables, se ele o espera no ambiente global.
window.jQuery = $;
window.$ = $;

// Você pode importar os módulos JS de integração do DataTables separadamente, se precisar
// import 'datatables.net-bs5/js/dataTables.bootstrap5.min.js'; // Exemplo para integração Bootstrap 5

// Seu código JS customizado
console.log('Vite está funcionando com Flask!');

// Exemplo: Inicializar DataTables
$(document).ready(function() {
    // Certifique-se de que DataTable foi carregado corretamente
    // Se você tiver uma tabela com o ID 'myTable'
    // Exemplo básico:
    // $('#myTable').DataTable();
});