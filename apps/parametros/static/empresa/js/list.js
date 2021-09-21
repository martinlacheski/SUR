$(function () {

    $('#data').DataTable({
        paging: false,
        searching: false,
        ordering: false,
        responsive: true,
        autoWidth: false,
        info: false,
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
            {"data": "cuit"},
            {"data": "email"},
            {"data": "telefono"},
            {"data": "email"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/empresa/view/' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fas fa-eye"></i></a> ';
                    buttons += '<a href="/empresa/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    }).on('click', 'a[rel="detalleEmpresa"]', function () {
        $('#detalleEmpresa').modal('show');
    });
});