var tablaProductos;
var tablaServicios;
var cantProductos = 0;
var cantServicios = 0;
$(function () {

    var tablaTrabajo = $('#data').DataTable({
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
            {"data": "id"},
            {"data": "id"},
            {"data": "fechaEntrada"},
            {"data": "fechaSalida"},
            {"data": "modelo.marca.nombre"},
            {"data": "modelo.nombre"},
            {"data": "cliente.razonSocial"},
            {"data": "total"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [0],
                class: 'text-center',
            },
            {
                targets: [1],
                class: 'text-center',
                render: function (data, type, row) {
                    if (row.estado) {
                        return '<span class="badge badge-success">' + ' Confirmado' + '</span>'
                    }
                    return '<span class="badge badge-danger">' + ' No confirmado' + '</span>'
                }
            },
            {
                targets: [-7],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return moment(moment(data, 'YYYY-MM-DD')).format('DD-MM-YYYY');
                }
            },
            {
                targets: [-6],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (row.fechaSalida) {
                        return moment(moment(data, 'YYYY-MM-DD')).format('DD-MM-YYYY');
                    } else {
                        return '<span class="badge badge-danger">' + ' Pendiente' + '</span>'
                    }
                }
            },
            {
                targets: [-3, -4, -5],
                class: 'text-center',
                orderable: false,
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
                    var buttons = '<a rel="detalleTrabajo" class="btn btn-success btn-xs btn-flat"><i class="fas fa-eye"></i></a> ';
                    buttons += '<a href="/trabajos/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    if (!row.fechaSalida) {
                        buttons += '<a href="/trabajos/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/trabajos/delete/' + row.id + '/" id="' + row.id + '" onclick="btnEliminar(this.id, this.href)" class="btn btn-danger btn-xs btn-flat" data-toggle="modal" data-target="#deleteModal"><i class="fas fa-times"></i>';
                    }
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

    $('#data tbody')
        .on('click', 'a[rel="detalleTrabajo"]', function () {
            //Seleccionamos el Presupuesto sobre la cual queremos traer el detalle
            var tr = tablaTrabajo.cell($(this).closest('td, li')).index();
            var data = tablaTrabajo.row(tr.row).data();

            //Cargamos el detalle de productos
            $('#tablaProductos').DataTable({
                responsive: true,
                autoWidth: false,
                info: false,
                searching: false,
                ordering: false,
                paging: false,
                destroy: true,
                deferRender: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': csrftoken,
                        'action': 'search_detalle_productos',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "producto.descripcion"},
                    {"data": "observaciones"},
                    {"data": "precio"},
                    {"data": "cantidad"},
                    {"data": "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [-2],
                        class: 'text-center',
                    },
                    {
                        targets: [-1, -3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                ],
                initComplete: function (settings, json) {
                    //Obtenemos la cantidad de ROWS en el datatables
                    cantProductos = json.length;
                    //Si no existen productos no mostramos en el modal la tabla
                    if (cantProductos < 1) {
                        document.getElementById("rowProductos").style.visibility = "collapse";
                    } else {
                        document.getElementById("rowProductos").style.visibility = "visible";
                    }
                }
            });
            //Cargamos el detalle de servicios
            $('#tablaServicios').DataTable({
                responsive: true,
                autoWidth: false,
                info: false,
                searching: false,
                ordering: false,
                paging: false,
                destroy: true,
                deferRender: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': csrftoken,
                        'action': 'search_detalle_servicios',
                        'id': data.id
                    },
                    dataSrc: "",
                },
                columns: [
                    {"data": "servicio.descripcion"},
                    {"data": "observaciones"},
                    {"data": "precio"},
                    {"data": "cantidad"},
                    {"data": "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [-2],
                        class: 'text-center',
                    },
                    {
                        targets: [-1, -3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                ],
                initComplete: function (settings, json) {
                    //Obtenemos la cantidad de ROWS en el datatables
                    cantServicios = json.length;
                    //Si no existen servicios no mostramos en el modal la tabla
                    if (cantServicios < 1) {
                        document.getElementById("rowServicios").style.visibility = "collapse";
                    } else {
                        document.getElementById("rowServicios").style.visibility = "visible";
                    }
                }
            });
            $('#modalDetalle').modal('show');
        });

});