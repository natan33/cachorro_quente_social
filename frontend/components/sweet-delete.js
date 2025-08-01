import Swal from 'sweetalert2';

/**
 * Componente de exclusão com SweetAlert2
 * @param {string} url - URL do recurso a ser deletado (ex: /api/sales/1)
 * @param {Function} onSuccess - Função a ser chamada após exclusão com sucesso
 * @param {string} mensagem - Texto opcional personalizado
 */
export function confirmDelete(url, onSuccess, mensagem = 'A ação não poderá ser desfeita!') {
  Swal.fire({
    title: 'Tem certeza?',
    text: mensagem,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#6c757d',
    confirmButtonText: 'Sim, excluir!',
    cancelButtonText: 'Cancelar'
  }).then((result) => {
    if (result.isConfirmed) {
      fetch(url, {
        method: 'DELETE'
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          Swal.fire('Excluído!', 'A exclusão foi realizada com sucesso.', 'success');
          if (onSuccess) onSuccess();
        } else {
          Swal.fire('Erro!', data.message || 'Não foi possível excluir.', 'error');
        }
      })
      .catch(() => {
        Swal.fire('Erro!', 'Ocorreu um erro ao tentar excluir.', 'error');
      });
    }
  });
}
