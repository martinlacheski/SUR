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
            {"data": "razonSocial"},
            {"data": "telefono"},
            {"data": "email"},
            {"data": "cuit"},
            {"data": "localidad.full_name"},
            {"data": "estado"},
            {"data": "email"},
        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    if (row.estado) {
                        return '<span class="badge badge-success">' + ' ACTIVO' + '</span>'
                    }
                    return '<span class="badge badge-danger">' + ' BAJA' + '</span>'
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/proveedores/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/proveedores/delete/' + row.id + '/" id="' + row.id + '" onclick="btnEliminar(this.id, this.href)" class="btn btn-danger btn-xs btn-flat" data-toggle="modal" data-target="#deleteModal"><i class="fas fa-trash-alt"></i>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});