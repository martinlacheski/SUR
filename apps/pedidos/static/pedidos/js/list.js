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
            {"data": "proveedor.razonSocial"},
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
                        return '<span class="badge badge-success">' + ' CONFIRMADO' + '</span>'
                    } else if (row.estado == false) {
                        return '<span class="badge badge-danger">' + ' CANCELADO' + '</span>'
                    } else {
                        return '<span class="badge badge-warning">' + ' NO CONFIRMADO' + '</span>'
                    }
                }
            },
            {
                targets: [2],
                class: 'text-center',
            },
            {
                targets: [3],
                class: 'text-center',
                // orderable: false,
                render: function (data, type, row) {
                    return moment(moment(data, 'YYYY-MM-DD')).format('DD-MM-YYYY');
                }
            },
            {
                targets: [-2, -3, -4, -5],
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
                    var buttons = '<a rel="detallePedido" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i></a> ';
                    buttons += '<a href="/pedidos/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
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
                        'action': 'search_detalle_pedido',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "producto.descripcion"},
                    {"data": "marcaOfertada"},
                    {"data": "costo"},
                    {"data": "cantidad"},
                    {"data": "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [1],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            if (row.marcaOfertada) {
                                return row.marcaOfertada
                            } else {
                                // return '<span class="badge badge-success">' + ' SIN OBSERVACIONES' + '</span>'
                                return 'SIN OBSERVACIONES'
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
                    $('input[name="subtotal"]').val(data.subtotal);
                    $('input[name="iva"]').val(data.iva);
                    $('input[name="total"]').val(data.total);
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