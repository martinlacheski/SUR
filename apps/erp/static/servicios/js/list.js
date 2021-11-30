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
            {"data": "descripcion"},
            {"data": "esfuerzo"},
            {"data": "codigo"},
            {"data": "imagen"},
            {"data": "precioVenta"},
            {"data": "precioVenta"}, //va duplicado algun campo por la botonera
        ],
        columnDefs: [
            {
                targets: [-5],
                class: 'text-center',
                render: function (data, type, row) {
                    var porcentaje = parseFloat(data).toFixed(2);
                    if (porcentaje <= 33.33) {
                        return '<span class="badge badge-success">' + data + '%' + '</span>'
                    } else if (porcentaje >= 33.34 && porcentaje <= 66.66) {
                        return '<span class="badge badge-warning">' + data + '%' + '</span>'
                    } else {
                        return '<span class="badge badge-danger">' + data + '%' + '</span>'
                    }
                }
            },
            {
                targets: [-4],
                class: 'text-center',
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 30px; height: 30px;">';
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
                    var buttons = '<a href="/servicios/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/servicios/delete/' + row.id + '/" id="' + row.id + '" onclick="btnEliminar(this.id, this.href)" class="btn btn-danger btn-xs btn-flat" data-toggle="modal" data-target="#deleteModal"><i class="fas fa-trash-alt"></i>';

                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});