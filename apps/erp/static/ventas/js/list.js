//Creamos una variable para cargar el SELECT de Clientes
var select_clientes = $('select[name="selectCliente"]');
var tablaProductos;
var tablaServicios;
var cantProductos = 0;
var cantServicios = 0;
$(function () {
    var tablaVenta = $('#data').DataTable({
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
            {"data": "estadoVenta"},
            {"data": "fecha"},
            {"data": "trabajo"},
            {"data": "cliente.razonSocial"},
            {"data": "subtotal"},
            {"data": "iva"},
            {"data": "percepcion"},
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
                // orderable: false,
                render: function (data, type, row) {
                    if (row.estadoVenta) {
                        return '<span class="badge badge-success">' + ' Realizada' + '</span>'
                    }
                    return '<span class="badge badge-danger">' + ' Cancelada' + '</span>'
                }
            },
            {
                targets: [-8],
                class: 'text-center',
                // orderable: false,
                render: function (data, type, row) {
                    return moment(moment(data, 'YYYY-MM-DD')).format('DD-MM-YYYY');
                }
            },
            {
                targets: [-7],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<span class="badge badge-primary">' + row.trabajo + '</span>'
                }
            },
            {
                targets: [-6],
                class: 'text-center',
                orderable: false,
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
                    var buttons = '<a rel="detalleVenta" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i></a> ';
                    buttons += '<a href="/ventas/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    if (row.estadoVenta) {
                        buttons += '<a href="/ventas/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/ventas/delete/' + row.id + '/" id="' + row.id + '" onclick="btnEliminar(this.id, this.href)" class="btn btn-danger btn-xs btn-flat" data-toggle="modal" data-target="#deleteModal"><i class="fas fa-times"></i>';
                    }
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {
            this.api().columns(4).every(function () {
                var column = this;
                var select = $('<select><option value=""></option></select>')
                    .appendTo($(column.footer()).empty())
                    .on('change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );

                        column
                            .search(val ? '^' + val + '$' : '', true, false)
                            .draw();
                    });
                var id = 1;
                column.data().unique().sort().each(function (d, j) {
                    var newOption = new Option(d.toString(), id, false, false);
                    $('.selectCliente').append(newOption).trigger('change');
                    id += 1;
                });
            });
        }
    });

    $('#data tbody')
        .on('click', 'a[rel="detalleVenta"]', function () {
            //Seleccionamos la Venta sobre la cual queremos traer el detalle
            var tr = tablaVenta.cell($(this).closest('td, li')).index();
            var data = tablaVenta.row(tr.row).data();
            //Buscamos el ID del Trabajo si es que tiene
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrftoken,
                    'action': 'search_TrabajoID',
                    'pk': data.id
                },
                dataType: 'json',
                success: function (data) {
                    var trabajo = data;
                    var ver = document.getElementById("trabajoID");
                    if (trabajo.trabajoID !== null && trabajo.trabajoID !== '' && trabajo.trabajoID !== undefined) {
                        ver.innerHTML = 'Detalle de Venta - ID Trabajo: ' + trabajo.trabajoID;
                    } else {
                        ver.innerHTML = 'Detalle de Venta ';
                    }
                }
            });
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
//------------------------------------FILTROS----------------------------------------//
    //Aplicamos Filtro de Rango de FECHAS
    $('input[name="filterRangoFechas"]').on('apply.daterangepicker', function (ev, picker) {
        //Extendemos la busqueda del datatables
        $.fn.dataTable.ext.search.push(
            function (settings, data, dataIndex) {
                //Asignamos las variables Desde y Hasta
                var desde = picker.startDate.format('YYYY-MM-DD');
                var hasta = picker.endDate.format('YYYY-MM-DD');
                // Asignamos el dia por cada renglon
                var dia = moment(moment(data[2], 'DD-MM-YYYY')).format('YYYY-MM-DD');
                //Comparamos contra el renglon
                if (desde <= dia && dia <= hasta) {
                    return true;
                }
                return false;
            }
        );
        //Actualizamos la tabla
        tablaVenta.draw();
    });
    //Reseteamos el Filtro de Fechas
    $('.btnClearRango').on('click', function () {
        $.fn.dataTable.ext.search = [];
        $.fn.dataTable.ext.search.pop();
        tablaVenta.draw();
    });
    //Aplicamos Filtro de Clientes
    $('.selectCliente').on('change', function () {
        //Asignamos a una variabla el cliente del Select
        var cliente = $(this).val();
        if (cliente !== null && cliente !== '' && cliente !== undefined) {
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el cliente por cada renglon
                    var clienteTabla = (data[4].toString());
                    console.log(cliente);
                    console.log(clienteTabla);
                    //Comparamos contra el renglon
                    if (cliente === clienteTabla) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaVenta.draw();
        }
    });
    //Reseteamos el Filtro de Fechas
    $('.btnClearRango').on('click', function () {
        $.fn.dataTable.ext.search = [];
        $.fn.dataTable.ext.search.pop();
        tablaVenta.draw();
    });
});

$(document).ready(function () {
    //Inicializamos SELECT2
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    //Inicializamos el Filtro de Rango de Fechas
    $('input[name="filterRangoFechas"]').daterangepicker({
        autoUpdateInput: false,
        locale: {
            placeholder: 'Seleccione Rango de Fechas',
            format: 'DD-MM-YYYY',
            language: 'es',
            cancelLabel: 'Cancelar',
            applyLabel: 'Aplicar',
        },
        //Remover Botones de Aplicar y Cancelar
        autoApply: true,
    });
    //Inicializamos limpio el Filtro de Rango de Fechas
    $('#filterRangoFechas').val('');
    //Extendemos el Datatables para asignar el formato de fecha
    $.fn.dataTable.moment('DD-MM-YYYY');
});

$(function () {
    var table = $('#data').DataTable();

});