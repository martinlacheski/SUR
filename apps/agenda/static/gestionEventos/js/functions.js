
// Inicialización de datimepicker
$('#fechaNotificacio').datetimepicker({
    format: 'DD-MM-yyyy',
    locale: 'es',
    icons: {date: 'far fa-calendar-alt'},
});

// Realiza un movimiento de modales. Nada wow
$('#btnDel').on('click', function() {
    $('#modal-lg-eventos').modal('hide'); // Escondemos el modal
    $('#deleteModal').modal('show') //Abrimos modal de confirmacion
});


// Toggle de activación de select
$('#customCheckbox1').on('click', function (){
    if (this.checked) {
        $('#selectRepeticion').prop('disabled', false);
    } else {
        $('#selectRepeticion').prop('disabled', true);
    }
});

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