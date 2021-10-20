var tablaProductos;
$(function () {
    var tablaPedido = $('#data').DataTable({
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
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "estado"},
            {"data": "fecha"},
            {"data": "subtotal"},
            {"data": "iva"},
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
                orderable: false,
                render: function (data, type, row) {
                    if (row.estado == true) {
                        return '<span class="badge badge-success">' + ' Confirmado' + '</span>'
                    } else if (row.estado == false) {
                        return '<span class="badge badge-danger">' + ' Cancelado' + '</span>'
                    } else {
                        return '<span class="badge badge-warning">' + ' No confirmado' + '</span>'
                    }
                }
            },
            {
                targets: [2],
                class: 'text-center',
                // orderable: false,
                render: function (data, type, row) {
                    return moment(moment(data, 'YYYY-MM-DD')).format('DD-MM-YYYY');
                }
            },
            {
                targets: [-2, -3, -4],
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
                    if (row.estado !== false && row.estado !== true) {
                        var buttons = '<a href="/pedidos/solicitudes/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/pedidos/solicitudes/confirm/' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fas fa-check"></i></a> ';
                        buttons += '<a href="/pedidos/solicitudes/delete/' + row.id + '/" id="' + row.id + '" onclick="btnEliminar(this.id, this.href)" class="btn btn-danger btn-xs btn-flat" data-toggle="modal" data-target="#deleteModal"><i class="fas fa-times"></i>';
                    } else {
                        var buttons = '<a rel="detallePedido" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i></a> ';
                        buttons += '<a href="/pedidos/solicitudes/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    }
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

    $('#data tbody')
        .on('click', 'a[rel="detallePedido"]', function () {
            //Seleccionamos la Solicitud de Pedido sobre la cual queremos traer el detalle
            var tr = tablaPedido.cell($(this).closest('td, li')).index();
            var data = tablaPedido.row(tr.row).data();
            //Cargamos el detalle de productos
            tablaProductos = $('#tablaProductos').DataTable({
                responsive: true,
                autoWidth: false,
                info: false,
                searching: false,
                //Ordenamos por grupo de producto
                order: [0, 'asc'],
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
                    {"data": "proveedor"},
                    {"data": "costo"},
                    {"data": "cantidad"},
                    {"data": "subtotal"},
                ],
                columnDefs: [
                    //Ocultamos la columna por la cual agrupamos
                    {"visible": false, "targets": 0},
                    {
                        targets: [-4],
                        class: 'text-center',
                        render: function (data, type, row) {
                            if (row.proveedor) {
                                return data.razonSocial;
                            } else {
                                return '';
                            }
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        orderable: false,
                    },
                    {
                        targets: [-1, -3],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                ],
                drawCallback: function (settings) {
                    var api = this.api();
                    var rows = api.rows({page: 'current'}).nodes();
                    var last = null;
                    api.column(0, {page: 'current'}).data().each(function (group, i) {
                        if (last !== group) {
                            $(rows).eq(i).before(
                                '<tr class="group"><td colspan="5">' + group + '</td></tr>'
                            );
                            last = group;
                        }
                    });
                },
                initComplete: function (settings, json) {
                }
            });
            $('#modalDetalle').modal('show');
        });

    // Ordenar por el Producto Agrupado
    $('#tablaProductos tbody').on('click', 'tr.group', function () {
        var currentOrder = tablaProductos.order()[0];
        if (currentOrder[0] === 0 && currentOrder[1] === 'asc') {
            tablaProductos.order([0, 'desc']).draw();
        } else {
            tablaProductos.order([0, 'asc']).draw();
        }
    });
});
$(document).ready(function () {
    //Extendemos el Datatables para asignar el formato de fecha
    $.fn.dataTable.moment('DD-MM-YYYY');
});