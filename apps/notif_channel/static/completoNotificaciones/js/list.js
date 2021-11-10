
$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        order: [0, 'desc'],
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'search_data'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "titulo"},
            {"data": "fechaNotificacion"},
            {"data": "estado"},
            {"data": "id"},

        ],
        columnDefs: [
            {
                targets: [0],
                class: 'text-center',
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return row.notificado;
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a id="' + row.id + '" onclick="detalleNotificacion(this)" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i></a>';
                    return buttons;
                }
            },
            {
                targets: [3],
                class: 'text-center',
                render: function (data, type, row) {
                    if (row.estado === 'vista') {
                        return '<span class="badge badge-success">' + row.estado.toUpperCase() + '</span>';
                    } else if (row.estado === 'pendiente') {
                         return '<span class="badge badge-warning">' + row.estado.toUpperCase() + '</span>';
                    } else if (row.estado === 'urgente'){
                        return '<span class="badge badge-danger">' + row.estado.toUpperCase() + '</span>';
                    } else if (row.estado === 'resuelta') {
                        return '<span class="badge badge-secondary">' + row.estado + '</span>';
                    }
                }
            }
        ],
        initComplete: function (settings, json) {

        }
    });
});

