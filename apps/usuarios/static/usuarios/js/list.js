$(function () {
    //Al hacer click en el AYUDA
    $('.verAyuda').on('click', function () {
        introJs().setOptions({
            showProgress: true,
            showBullets: false,
            nextLabel: 'Siguiente',
            prevLabel: 'Atrás',
            doneLabel: 'Finalizar',
        }).start()
    });

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
            {"data": "full_name"},
            {"data": "username"},
            {"data": "cuil"},
            {"data": "email"},
            {"data": "telefono"},
            {"data": "is_active"},
            // {"data": "imagen"},
            {"data": "realizaTrabajos"},
            {"data": "username"},
        ],
        columnDefs: [
            {
                targets: [-3],
                class: 'text-center',
                render: function (data, type, row) {
                    if (row.is_active) {
                        return '<span class="badge badge-success">' + ' ACTIVO' + '</span>'
                    }
                    return '<span class="badge badge-danger">' + ' BAJA' + '</span>'
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    //     return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 30px; height: 30px;">';
                    // }
                    if (row.realizaTrabajos) {
                        return '<span class="badge badge-success">' + ' SI' + '</span>'
                    }
                    return '<span class="badge badge-danger">' + ' NO' + '</span>'
                    }
                },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/usuarios/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/usuarios/delete/' + row.id + '/" id="' + row.id + '" onclick="btnEliminar(this.id, this.href)" class="btn btn-danger btn-xs btn-flat" data-toggle="modal" data-target="#deleteModal"><i class="fas fa-trash-alt"></i>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
})
    ;