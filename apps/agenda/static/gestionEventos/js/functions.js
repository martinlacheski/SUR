
// Inicialización de datimepicker


// Realiza un movimiento de modales. Nada wow
$('#btnDel').on('click', function() {
    $('#modal-lg-eventos').modal('hide'); // Escondemos el modal
    $('#deleteModal').modal('show') //Abrimos modal de confirmacion
});


// Toggle de activación de select y de fecha de finalización


// Checkbox marcada en caso de que estémos en una update page
$(document).ready( function () {
    if(window.location.pathname.includes('updateEvento')){
        $("#customCheckbox1").prop("checked", true);
        $('#selectRepeticion').prop('disabled', false);
    }
});


// Activación de select2
$('.form-select').select2({
    theme: "bootstrap4",
    language: 'es'
});