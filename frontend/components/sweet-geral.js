import Swal from 'sweetalert2';

export function showAlert({ icon = 'info', title = '', text = '', timer = null }) {
  return Swal.fire({
    icon,
    title,
    text,
    timer,       // Se quiser fechar automático
    timerProgressBar: timer ? true : false,
    showConfirmButton: !timer,
  });
}

