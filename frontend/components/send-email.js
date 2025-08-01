import $ from 'jquery';
import Swal from 'sweetalert2';

export function exportToExcel() {
    // Criar um array para armazenar os e-mails
    let emailArray = [];

    // Adiciona o e-mail ao pressionar Enter
    $('#email').on('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Impede a quebra de linha

            let value = $(this).val().trim();

            // Verifica se o valor contém "@" e "." (indicando que é um e-mail válido)
            if (value.includes('@') && value.includes('.')) {
                // Adiciona o e-mail à lista de e-mails
                emailArray.push(value);

                // Exibe o e-mail no modal
                $('#emailListDisplay').append(`<span class="badge bg-primary m-1">${value}</span>`);

                // Limpa o campo de entrada de e-mail
                $(this).val('');

                // Habilita o botão de envio se houver e-mails na lista
                if (emailArray.length > 0) {
                    $('#sendBtn').prop('disabled', false);
                }
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Erro',
                    text: 'Por favor, insira um e-mail válido.',
                });
            }
        }
    });

    // Ação ao enviar o formulário
    $('#sendExcelForm').on('submit', function(event) {
        event.preventDefault(); // Evita que o formulário seja enviado de forma tradicional

        // Verifica se há e-mails inseridos
        if (emailArray.length > 0) {
            // Enviar os dados para o servidor via fetch
            const data = {
                emails: emailArray
            };

            // Requisição POST para o servidor
            fetch('/api/send_excel', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Sucesso!',
                        text: `E-mails enviados para: ${emailArray.join(', ')}`,
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Erro',
                        text: 'Erro ao enviar os e-mails: ' + data.message,
                    });
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Erro',
                    text: 'Ocorreu um erro ao tentar enviar os e-mails. Tente novamente.',
                });
            });

            // Fechar o modal após o envio
            $('#sendExcelModal').modal('hide');
        } else {
            // Caso não tenha e-mails
            Swal.fire({
                icon: 'warning',
                title: 'Atenção',
                text: 'Por favor, insira pelo menos um e-mail.',
            });
        }
    });
}
