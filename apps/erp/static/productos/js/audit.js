var tablaProductos;
//Creamos variables auxiliares para el reporte
var fechaInicio = '';
var fechaFin = '';
var checkCanceladas = true;
//Creamos una estructura para el Reporte
var reporte = {
    items: {
        //Filtros
        producto: '',
        usuario: '',
        fechaDesde: '',
        fechaHasta: '',
        //detalle de compras
        productos: [],
    },
};
$(function () {
    tablaProductos = $('#data').DataTable({
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
            {"data": "descripcion"},
            {"data": "stockReal"},
            {"data": "precioVenta"},
            {"data": "history_type"},
            {"data": "history_user"},
            {"data": "history_id"}, //va duplicado algun campo por la botonera
        ],
        columnDefs: [
            {
                targets: [-8, -2],
                class: 'text-center',
            },
            {
                targets: [-7],
                class: 'text-center',
                render: function (data, type, row) {
                    return moment(moment(data, 'YYYY-MM-DD HH:mm')).format('DD-MM-YYYY HH:mm');
                }

            },
            {
                targets: [-5],
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
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (row.history_type == '+') {
                        var buttons = '<a class="btn btn-primary btn-xs btn-flat readonly"><i class="fas fa-plus"></i></a> ';
                        return buttons
                    } else if (row.history_type == '~') {
                        var buttons = '<a class="btn btn-warning btn-xs btn-flat readonly"><i class="fas fa-edit"></i></a> ';
                        return buttons
                    } else if (row.history_type == '-') {
                        var buttons = '<a class="btn btn-danger btn-xs btn-flat readonly"><i class="fas fa-minus"></i></a> ';
                        return buttons
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
            //Agregamos al Select2 los Productos que tenemos en el listado
            this.api().columns(2).every(function () {
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
                    $('.selectProducto').append(newOption).trigger('change');
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
            tablaProductos.draw();
        }
    });
    $('#data tbody')
        .on('click', 'a[rel="detalleMovimiento"]', function () {
            //Seleccionamos el Producto sobre la cual queremos traer el detalle
            var tr = tablaProductos.cell($(this).closest('td, li')).index();
            var data = tablaProductos.row(tr.row).data();
            //Realizamos el AJAX para buscar el DETALLE DE LA AUDITORIA

            $('#modalProducto').modal('show');
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
        tablaProductos.draw();
    });

    //Aplicamos Filtro de Productos
    $('.selectProducto').on('change', function () {
        //Reseteamos los filtros
        $.fn.dataTable.ext.search = [];
        $.fn.dataTable.ext.search.pop();
        tablaProductos.draw();
        //Asignamos a una variabla el producto del Select
        var producto = $(this).val();
        if (producto !== null && producto !== '' && producto !== undefined) {
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el producto por cada renglon
                    var productoTabla = (data[2].toString());
                    //Comparamos contra el renglon
                    if (producto === productoTabla) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaProductos.draw();
        }
    });

    //Aplicamos Filtro de Usuarios
    $('.selectUsuario').on('change', function () {
        //Reseteamos los filtros
        $.fn.dataTable.ext.search = [];
        $.fn.dataTable.ext.search.pop();
        tablaProductos.draw();
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
            tablaProductos.draw();
        }
    });

    //Boton Resetear Filtros
    $('.btnResetFilters').on('click', function () {
        $.fn.dataTable.ext.search = [];
        $.fn.dataTable.ext.search.pop();
        tablaProductos.draw();
        $('.selectProducto').val(null).trigger('change');
        $('.selectUsuario').val(null).trigger('change');
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
        reporte.items.producto = $('select[name="selectProducto"]').val();
        reporte.items.usuario = $('select[name="selectUsuario"]').val();
        reporte.items.fechaDesde = fechaInicio;
        reporte.items.fechaHasta = fechaFin;
        reporte.items.productos = dataAuditoria;
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
                    console.log(data.error);
                }
            }
        });
    });
});
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