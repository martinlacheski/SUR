/*  Traduce los valores por defecto. Utilizada debido a la implementación de BooleanFields
    los cuales son más sencillos de implementar con elemento toggle */
function simple_traduc(data){
    var mod_data = '';
    if(data === true){
        mod_data = 'Sí';
    }else{
        mod_data = 'No';
    }
    return mod_data;
}

$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "nombre"},
            {"data": "horarioRecordatorio"},
            {"data": "recordarSistema"},
            {"data": "recordarTelegram"},
            {"data": "usuariosAsoc"},
            {"data": "nombre"}, //va duplicado algun campo por la botonera

        ],
        columnDefs: [
            {
                targets: [5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/agenda/tiposEventos/edit/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/agenda/tiposEventos/delete/' + row.id + '/" id="' + row.id +'" onclick="btnEliminar(this.id, this.href)" class="btn btn-danger btn-xs btn-flat" data-toggle="modal" data-target="#deleteModal"><i class="fas fa-trash-alt"></i>';
                    return buttons;
                }
            },
            {
                targets: [2],
                render: function (data, type, row){
                    return simple_traduc(data);
                }
            },
            {
                targets: [3],
                render: function (data, type, row){
                    return simple_traduc(data);
                }
            },


        ],
        initComplete: function (settings, json) {

        }
    });
});

