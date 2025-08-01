import $ from 'jquery';

// saleDetailsModal.js
import * as bootstrap from 'bootstrap';
import Swal from 'sweetalert2';
import { showAlert } from '../components/sweet-geral';


export function eventFormEditVenda() {


    const form = $('#saleFormEdit');
    const modal = form.closest('.modal');
    const modalId = modal.attr('id');

    const product = {
        id: 1,
        name: "Cachorro Quente",
        price: 5.00
    };

    let saleId = null;

    $('#salesTable tbody').on('click', '.edit-sale', function () {
        // Pega o Id da linha da tabela
        saleId = $(this).data('id');
    });


    function updateTotal() {
        let quantity = parseInt($('#quantityEdite').val()) || 1;
        let total = product.price * quantity;
        $('#totalAmountIdeti').text(`R$ ${total.toFixed(2)}`);
    }

    $('#quantityEdite').on('input change', updateTotal);

    $(form).on('submit', function (e) {
        e.preventDefault();

        // Pega o Id da linha da tabela

        const dados = form.serializeArray();
        dados.push({
            name: 'id_atual',
            value: saleId // ou qualquer valor dinâmico
        });
        $.ajax({
            url: form.attr("action") || "/api/edit_sale",
            type: form.attr("method") || "POST",
            data: dados,
            success: function (response) {

                form[0].reset();

                $("#salesTable").DataTable().ajax.reload();

                $('#fechar-modal-edit-venda').trigger('click');

                Swal.fire({ title: "Pedido Editado com sucesso!", icon: "success", timer: 1000, showConfirmButton: false });
                //(modalId)
                setTimeout(() => {
                    Swal.close();

                }, 1600);

            },
            error: function () {
                Swal.fire("Oops!", "Erro ao enviar formulário!", "error");
            }

        });

    });
}