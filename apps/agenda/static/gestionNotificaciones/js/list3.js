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
    var buttons;
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
            {"data": "diasAntelacion"},
            {"data": "lunes"},
            {"data": "martes"},
            {"data": "miercoles"},
            {"data": "jueves"},
            {"data": "viernes"}, //va duplicado algun campo por la botonera
            {"data": "sabado"}, //va duplicado algun campo por la botonera
            {"data": "domingo"}, //va duplicado algun campo por la botonera
            {"data": "diasAntelacion"}, //va duplicado algun campo por la botonera //va duplicado algun campo por la botonera

        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    buttons = '<a href="/agenda/gestionNotif/edit/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    return buttons;
                }
            },
            {
                targets:[1, 2, 3, 4, 5, 6, 7],
                render: function (data, type, row){
                    return simple_traduc(data);
                }

            },
        ],
        initComplete: function (settings, json) {

        }
    });
});


