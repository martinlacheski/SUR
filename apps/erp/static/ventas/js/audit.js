var tablaVentas;
//Creamos variables auxiliares para el reporte
var fechaInicio = '';
var fechaFin = '';
var checkCanceladas = true;
//Creamos una estructura para el Reporte
var reporte = {
    items: {
        //Filtros
        venta: '',
        accion: '',
        usuario: '',
        fechaDesde: '',
        fechaHasta: '',
        //detalle de ventas
        ventas: [],
    },
};
$(function () {
    //Al hacer click en el AYUDA
    $('.verAyuda').on('click', function () {
        document.getElementById("filters").style.display = "";
        introJs().setOptions({
            showProgress: true,
            showBullets: false,
            nextLabel: 'Siguiente',
            prevLabel: 'Atrás',
            doneLabel: 'Finalizar',
        }).start()
    });

    tablaVentas = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        paging: true,
        order: [0, 'desc'],
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
            {"data": "history_id"},
            {"data": "history_date"},
            {"data": "venta_id"},
            {"data": "cliente"},
            {"data": "trabajo"},
            {"data": "history_type"},
            {"data": "history_user"},
            {"data": "history_id"}, //va duplicado algun campo por la botonera
        ],
        columnDefs: [
            {
                targets: [-5, -2],
                class: 'text-center',
            },
            {
                targets: [1],
                class: 'text-center',
                render: function (data, type, row) {
                    return moment(moment(data, 'YYYY-MM-DD HH:mm')).format('DD-MM-YYYY HH:mm');
                }

            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (row.history_type == '+') {
                        return 'Creación'
                    } else if (row.history_type == '~') {
                        return 'Actualización'
                    } else if (row.history_type == '-') {
                        return 'Eliminación'
                    }
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="detalleMovimiento" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {
            //Agregamos al Select2 los Clientes que tenemos en el listado
            this.api().columns(3).every(function () {
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
                column.data().unique().sort().each(function (d, j) {
                    var newOption = new Option(d.toString(), d.toString(), false, false);
                    $('.selectCliente').append(newOption).trigger('change');
                });
            });
            //Agregamos al Select2 las acciones que tenemos en el listado
            this.api().columns(5).every(function () {
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
                column.data().unique().sort().each(function (d, j) {
                    var option = d.toString();
                    if (option === '+') {
                        option = 'Creación';
                    } else if (option === '-') {
                        option = 'Eliminación';
                    } else if (option === '~') {
                        option = 'Actualización';
                    }
                    var newOption = new Option(option, option, false, false);
                    // var newOption = new Option(d.toString(), d.toString(), false, false);
                    $('.selectAccion').append(newOption).trigger('change');
                });
            });
            //Agregamos al Select2 los Usuarios que tenemos en el listado
            this.api().columns(6).every(function () {
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
                column.data().unique().sort().each(function (d, j) {
                    var newOption = new Option(d.toString(), d.toString(), false, false);
                    $('.selectUsuario').append(newOption).trigger('change');
                });
            });
            //Actualizamos la tabla
            tablaVentas.draw();
        }
    });
    $('#data tbody')
        .on('click', 'a[rel="detalleMovimiento"]', function () {
            //Asignamos a una variable el renglon que necesitamos
            var tr = tablaVentas.cell($(this).closest('td, li')).index();
            renglon = tr.row;
            //Asignamos a una variable el movimiento en base al renglon
            var audit = tablaVentas.row(tr.row).data();
            //Realizamos el AJAX para buscar el DETALLE DE LA AUDITORIA
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'view_movimiento',
                    'pk': audit.history_id,
                    'venta_id': audit.venta_id,
                },
                dataType: 'json',
                headers: {
                    'X-CSRFToken': csrftoken
                },
            }).done(function (data) {
                var dato = data[0];
                //Cargamos los datos del Producto y mostramos en el modal con las modificaciones
                var idVenta = $('#modalId').val(dato.venta_id);
                var cliente = $('#modalCliente').val(dato.cliente);
                var condicion = $('#modalCondicion').val(dato.condicionVenta);
                var medioPago = $('#modalMedioPago').val(dato.medioPago);
                var fecha = $('#modalFecha').val(moment(moment(dato.fecha), 'YYYY-MM-DD').format('DD-MM-YYYY'));
                var subtotal = $('#modalSubtotal').val(dato.subtotal);
                var iva = $('#modalIva').val(dato.iva);
                var percepcion = $('#modalPercepcion').val(dato.percepcion);
                var total = $('#modalTotal').val(dato.total);
                if (audit.history_type === '~') {
                    var clienteOld = document.getElementById('modalClienteOld');
                    clienteOld.innerHTML = dato.clienteOld;
                    var condicionOld = document.getElementById('modalCondicionOld');
                    condicionOld.innerHTML = dato.condicionVentaOld;
                    var medioPagoOld = document.getElementById('modalMedioPagoOld');
                    medioPagoOld.innerHTML = dato.medioPagoOld;
                    var fechaOld = document.getElementById('modalFechaOld');
                    fechaOld.innerHTML = moment(moment(dato.fechaOld), 'YYYY-MM-DD').format('DD-MM-YYYY');
                    var subtotalOld = document.getElementById('modalSubtotalOld');
                    subtotalOld.innerHTML = dato.subtotalOld;
                    var ivaOld = document.getElementById('modalIvaOld');
                    ivaOld.innerHTML = dato.ivaOld;
                    var percepcionOld = document.getElementById('modalPercepcionOld');
                    percepcionOld.innerHTML = dato.percepcionOld;
                    var totalOld = document.getElementById('modalTotalOld');
                    totalOld.innerHTML = dato.totalOld;
                    if (cliente.val() !== clienteOld.innerHTML) {
                        clienteOld.innerHTML = 'Valor anterior: ' + clienteOld.innerHTML
                        $("#modalClienteOld").removeAttr("hidden");
                    }
                    if (condicion.val() !== condicionOld.innerHTML) {
                        condicionOld.innerHTML = 'Valor anterior: ' + condicionOld.innerHTML
                        $("#modalCondicionOld").removeAttr("hidden");
                    }
                    if (medioPago.val() !== medioPagoOld.innerHTML) {
                        medioPagoOld.innerHTML = 'Valor anterior: ' + medioPagoOld.innerHTML
                        $("#modalMedioPagoOld").removeAttr("hidden");
                    }
                    if (fecha.val() !== fechaOld.innerHTML) {
                        fechaOld.innerHTML = 'Valor anterior: ' + fechaOld.innerHTML
                        $("#modalFechaOld").removeAttr("hidden");
                    }
                    if (subtotal.val() !== subtotalOld.innerHTML) {
                        subtotalOld.innerHTML = 'Valor anterior: $' + subtotalOld.innerHTML
                        $("#modalSubtotalOld").removeAttr("hidden");
                    }
                    if (iva.val() !== ivaOld.innerHTML) {
                        ivaOld.innerHTML = 'Valor anterior: $' + ivaOld.innerHTML
                        $("#modalIvaOld").removeAttr("hidden");
                    }
                    if (percepcion.val() !== percepcionOld.innerHTML) {
                        percepcionOld.innerHTML = 'Valor anterior: $' + percepcionOld.innerHTML
                        $("#modalPercepcionOld").removeAttr("hidden");
                    }
                    if (total.val() !== totalOld.innerHTML) {
                        totalOld.innerHTML = 'Valor anterior: $' + totalOld.innerHTML
                        $("#modalTotalOld").removeAttr("hidden");
                    }
                }
                //Cargamos el detalle de productos
                var productos = dato.detalle_productos;
                tablaProductos = $('#tablaProductos').DataTable({
                    paging: false,
                    searching: false,
                    // ordering: false,
                    //info: false,
                    responsive: true,
                    lengthMenu: [25, 50, 75, 100],
                    order: [2, 'asc'],
                    autoWidth: false,
                    destroy: true,
                    data: productos,
                    //Agregamos el Corte de Control para visualizar el estado anterior
                    createdRow: function (row, data, dataIndex) {
                        if (data.history_type === "-") {
                            $(row).addClass("highlight");
                        }
                    },
                    columns: [
                        {"data": "history_id"},
                        {"data": "history_date"},
                        {"data": "producto"},
                        {"data": "precio"},
                        {"data": "cantidad"},
                        {"data": "subtotal"},
                        {"data": "history_type"},
                        {"data": "usuario"},
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
                                return moment(moment(data, 'YYYY-MM-DD HH:mm')).format('DD-MM-YYYY HH:mm');
                            }

                        },
                        {
                            targets: [-6, -4],
                            class: 'text-center',
                            orderable: false,
                        },
                        {
                            targets: [-5, -3],
                            class: 'text-right',
                            orderable: false,
                            render: function (data, type, row) {
                                return '$' + parseFloat(data).toFixed(2);
                            }
                        },
                        {
                            targets: [-2],
                            class: 'text-center',
                            orderable: false,
                            render: function (data, type, row) {
                                if (row.history_type == '+') {
                                    return 'Actual'
                                } else if (row.history_type == '~') {
                                    return 'Actualización'
                                } else if (row.history_type == '-') {
                                    return 'Anterior'
                                }
                            },
                        },
                        {
                            targets: [-1],
                            class: 'text-center',
                            render: function (data, type, row) {
                                if (row.history_type == '-') {
                                    return dato.usuarioOld
                                } else {
                                    return dato.usuario
                                }
                            }
                        },
                    ],
                    initComplete: function (settings, json) {

                    }
                })
                ;
                //Cargamos el detalle de servicios
                var servicios = dato.detalle_servicios;
                tablaProductos = $('#tablaServicios').DataTable({
                    paging: false,
                    searching: false,
                    // ordering: false,
                    //info: false,
                    responsive: true,
                    lengthMenu: [25, 50, 75, 100],
                    order: [2, 'asc'],
                    autoWidth: false,
                    destroy: true,
                    data: servicios,
                    //Agregamos el Corte de Control para visualizar el estado anterior
                    createdRow: function (row, data, dataIndex) {
                        if (data.history_type === "-") {
                            $(row).addClass("highlight");
                        }
                    },
                    columns: [
                        {"data": "history_id"},
                        {"data": "history_date"},
                        {"data": "servicio"},
                        {"data": "precio"},
                        {"data": "cantidad"},
                        {"data": "subtotal"},
                        {"data": "history_type"},
                        {"data": "usuario"},
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
                                return moment(moment(data, 'YYYY-MM-DD HH:mm')).format('DD-MM-YYYY HH:mm');
                            }

                        },
                        {
                            targets: [-6, -4],
                            class: 'text-center',
                            orderable: false,
                        },
                        {
                            targets: [-5, -3],
                            class: 'text-right',
                            orderable: false,
                            render: function (data, type, row) {
                                return '$' + parseFloat(data).toFixed(2);
                            }
                        },
                        {
                            targets: [-2],
                            class: 'text-center',
                            orderable: false,
                            render: function (data, type, row) {
                                if (row.history_type == '+') {
                                    return 'Actual'
                                } else if (row.history_type == '~') {
                                    return 'Actualización'
                                } else if (row.history_type == '-') {
                                    return 'Anterior'
                                }
                            },
                        },
                        {
                            targets: [-1],
                            class: 'text-center',
                            render: function (data, type, row) {
                                if (row.history_type == '-') {
                                    return dato.usuarioOld
                                } else {
                                    return dato.usuario
                                }
                            }
                        },
                    ],
                    initComplete: function (settings, json) {

                    }
                });
            }).fail(function (jqXHR, textStatus, errorThrown) {
            }).always(function (data) {
            });
            $('#modalVenta').modal('show');
        });
//Al cerrar el Modal de Movimiento reseteamos los valores del formulario
    $('#modalVenta').on('hidden.bs.modal', function (e) {
        //Reseteamos los input del Modal
        $('#formVenta').trigger('reset');
        $('.spanForm').attr("hidden", true);
    });
//------------------------------------FILTROS----------------------------------------//
//Mostramos los Filtros
    $('.showFilters').on('click', function () {
        var filtros = $('#filters');
        if (filtros.css('display') === 'none') {
            document.getElementById("filters").style.display = "";
        } else {
            document.getElementById("filters").style.display = "none";
        }
    });
//Aplicamos Filtro de Rango de FECHAS
    $('input[name="filterRangoFechas"]').on('apply.daterangepicker', function (ev, picker) {
        //Extendemos la busqueda del datatables
        $.fn.dataTable.ext.search.push(
            function (settings, data, dataIndex) {
                //Asignamos las variables Desde y Hasta
                var desde = picker.startDate.format('YYYY-MM-DD');
                var hasta = picker.endDate.format('YYYY-MM-DD');
                fechaInicio = moment(moment(desde), 'DD-MM-YYYY').format('DD-MM-YYYY');
                fechaFin = moment(moment(hasta), 'DD-MM-YYYY').format('DD-MM-YYYY');
                // Asignamos el dia por cada renglon
                var dia = moment(moment(data[1], 'DD-MM-YYYY')).format('YYYY-MM-DD');
                //Comparamos contra el renglon
                if (desde <= dia && dia <= hasta) {
                    return true;
                }
                return false;
            }
        );
        //Actualizamos la tabla
        tablaVentas.draw();
    });
//Aplicamos Filtro de Productos
    $('.selectCliente').on('change', function () {
        //Asignamos a una variabla el producto del Select
        var producto = $(this).val();
        if (producto !== null && producto !== '' && producto !== undefined) {
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el producto por cada renglon
                    var productoTabla = (data[3].toString());
                    //Comparamos contra el renglon
                    if (producto === productoTabla) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaVentas.draw();
        }
    });
//Aplicamos Filtro de Accion
    $('.selectAccion').on('change', function () {
        //Asignamos a una variabla el usuario del Select
        var accion = $(this).val();
        if (accion !== null && accion !== '' && accion !== undefined) {
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el usuario por cada renglon
                    var accionTabla = (data[5].toString());
                    //Comparamos contra el renglon
                    if (accion === accionTabla) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaVentas.draw();
        }
    });
//Aplicamos Filtro de Usuarios
    $('.selectUsuario').on('change', function () {
        //Asignamos a una variabla el usuario del Select
        var usuario = $(this).val();
        if (usuario !== null && usuario !== '' && usuario !== undefined) {
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el usuario por cada renglon
                    var usuarioTabla = (data[6].toString());
                    //Comparamos contra el renglon
                    if (usuario === usuarioTabla) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaVentas.draw();
        }
    });

//Boton Resetear Filtros
    $('.btnResetFilters').on('click', function () {
        $.fn.dataTable.ext.search = [];
        $.fn.dataTable.ext.search.pop();
        tablaVentas.draw();
        $('.selectCliente').val(null).trigger('change');
        $('.selectUsuario').val(null).trigger('change');
        $('.selectAccion').val(null).trigger('change');
        //Limpiamos limpio el Filtro de Rango de Fechas
        $('input[name="filterRangoFechas"]').val('');
        fechaInicio = '';
        fechaFin = '';
    });
//------------------------------------GENERAR REPORTE----------------------------------------//
//Boton Generar Reporte
    $('#reporteForm').on('submit', function (e) {
        e.preventDefault();
        var dataAuditoria = [];
        //Recorremos el listado del Datatables para pasar el detalle con LOS FILTROS APLICADOS
        $('#data').DataTable().rows({filter: 'applied'}).every(function (rowIdx, tableLoop, rowLoop) {
            var data = this.data();
            dataAuditoria.push(data);
        });
        for (var i = 0; i < dataAuditoria.length; i++) {
            dataAuditoria[i].history_date = moment(moment(dataAuditoria[i].history_date, 'YYYY-MM-DD HH:mm')).format('DD-MM-YYYY HH:mm');
        }
        //Asignamos las variables a la estructura
        reporte.items.venta = $('select[name="selectVenta"]').val();
        reporte.items.accion = $('select[name="selectAccion"]').val();
        reporte.items.usuario = $('select[name="selectUsuario"]').val();
        reporte.items.fechaDesde = fechaInicio;
        reporte.items.fechaHasta = fechaFin;
        reporte.items.ventas = dataAuditoria;
        var parameters = new FormData();
        //Pasamos la accion
        parameters.append('action', 'create_reporte');
        parameters.append('reporte', JSON.stringify(reporte.items));
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            processData: false,
            contentType: false,
            success: function (data) {
                if (!data.hasOwnProperty('error')) {
                    //Abrimos el PDF en una nueva pestaña
                    window.open(data.url, '_blank');
                    location.reload();
                } else {
                    // console.log(data.error);
                }
            }
        });
    });
})
;
//------------------------------------Inicializar COMPONENTES----------------------------------------//
$(document).ready(function () {
    //Ocultamos los Filtros
    document.getElementById("filters").style.display = "none";
    //Inicializamos SELECT2
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    //Inicializamos el Filtro de Rango de Fechas
    $('input[name="filterRangoFechas"]').daterangepicker({
        // autoUpdateInput: false,
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
    //Extendemos el Datatables para asignar el formato de fecha
    $.fn.dataTable.moment('DD-MM-YYYY');
    //Inicializamos limpio el Filtro de Rango de Fechas
    $('input[name="filterRangoFechas"]').val('');
});