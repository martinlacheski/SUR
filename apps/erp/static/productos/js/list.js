$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        paging: true,
        // dom: 'Bfrtip',
        // buttons: [
        //     {
        //         extend: 'pdfHtml5',
        //         // orientation: 'landscape',
        //         orientation: 'vertical',
        //         pageSize: 'A4'
        //     }
        // ],
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
            {"data": "descripcion"},
            {"data": "codigo"},
            {"data": "codigoProveedor"},
            {"data": "imagen"},
            {"data": "stockReal"},
            {"data": "precioVenta"},
            {"data": "precioVenta"}, //va duplicado algun campo por la botonera
        ],
        columnDefs: [
            {
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 30px; height: 30px;">';
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (row.stockReal > 0) {
                        return '<span class="badge badge-success">' + data + '</span>'
                    }
                    return '<span class="badge badge-danger">' + data + '</span>'
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/productos/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/productos/delete/' + row.id + '/" id="' + row.id + '" onclick="btnEliminar(this.id, this.href)" class="btn btn-danger btn-xs btn-flat" data-toggle="modal" data-target="#deleteModal"><i class="fas fa-trash-alt"></i>';

                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});