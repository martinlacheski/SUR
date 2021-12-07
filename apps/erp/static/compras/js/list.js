//Creamos una variable para cargar el SELECT de Proveedores
var select_proveedores = $('select[name="selectProveedor"]');
var tablaProductos;
//Creamos variables auxiliares para el reporte
var fechaInicio = '';
var fechaFin = '';
var checkCanceladas = true;
//Creamos una estructura para el Reporte
var reporte = {
    items: {
        //Filtros
        proveedor: '',
        fechaDesde: '',
        fechaHasta: '',
        excluirCanceladas: '',
        //detalle de compras
        compras: [],
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
    var tablaCompra = $('#data').DataTable({
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
            {"data": "estadoCompra"},
            {"data": "fecha"},
            {"data": "proveedor.razonSocial"},
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
                orderable: false,
                render: function (data, type, row) {
                    if (row.estadoCompra) {
                        return '<span class="badge badge-success">' + ' REALIZADA' + '</span>'
                    }
                    return '<span class="badge badge-danger">' + ' CANCELADA' + '</span>'
                }
            },
            {
                targets: [-7],
                class: 'text-center',
                // orderable: false,
                render: function (data, type, row) {
                    return moment(moment(data, 'YYYY-MM-DD')).format('DD-MM-YYYY');
                }
            },
            {
                targets: [-6],
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
                    var buttons = '<a rel="detalleCompra" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i></a> ';
                    buttons += '<a href="/compras/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    if (row.estadoCompra) {
                        // buttons += '<a href="/compras/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/compras/delete/' + row.id + '/" id="' + row.id + '" onclick="btnEliminar(this.id, this.href)" class="btn btn-danger btn-xs btn-flat" data-toggle="modal" data-target="#deleteModal"><i class="fas fa-times"></i>';
                    }
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {
            //Agregamos al Select2 los Proveedores que tenemos en el listado
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
                    $('.selectProveedor').append(newOption).trigger('change');
                });
            });
            //Excluimos los cancelados
            var verdadero = ' CANCELADA';
            //Asignamos Verdadero a la variable auxiliar del reporte
            checkCancelados = true;
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el estado por cada renglon
                    var estado = (data[1]);
                    //Comparamos contra el renglon
                    if (verdadero === estado) {
                        return false;
                    }
                    return true;
                }
            );
            //Actualizamos la tabla
            tablaCompra.draw();
        }
    });

    $('#data tbody')
        .on('click', 'a[rel="detalleCompra"]', function () {
            //Seleccionamos la COMPRA sobre la cual queremos traer el detalle
            var tr = tablaCompra.cell($(this).closest('td, li')).index();
            var data = tablaCompra.row(tr.row).data();

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
                    {"data": "costo"},
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
                }
            });
            $('#modalDetalle').modal('show');
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
                var dia = moment(moment(data[2], 'DD-MM-YYYY')).format('YYYY-MM-DD');
                //Comparamos contra el renglon
                if (desde <= dia && dia <= hasta) {
                    return true;
                }
                return false;
            }
        );
        //Actualizamos la tabla
        tablaCompra.draw();
    });

    //Aplicamos Filtro de Proveedores
    $('.selectProveedor').on('change', function () {
        //Reseteamos los filtros
        $.fn.dataTable.ext.search = [];
        $.fn.dataTable.ext.search.pop();
        // tablaCompra.draw();
        //Limpiamos limpio el Filtro de Rango de Fechas
        $('input[name="filterRangoFechas"]').val('');
        fechaInicio = '';
        fechaFin = '';
        //Asignamos a una variabla el proveedor del Select
        var proveedor = $(this).val();
        if (proveedor !== null && proveedor !== '' && proveedor !== undefined) {
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el cliente por cada renglon
                    var proveedorTabla = (data[3].toString());
                    //Comparamos contra el renglon
                    if (proveedor === proveedorTabla) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaCompra.draw();
            $('#excluirCanceladas').prop('checked', false);
        }
    });
    //Filtrar Estado Canceladas
    $('#excluirCanceladas').on('click', function () {
        var verdadero = ' CANCELADA';
        if (this.checked) {
            //Asignamos Verdadero a la variable auxiliar del reporte
            checkCanceladas = true;
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el estado por cada renglon
                    var estado = (data[1]);
                    //Comparamos contra el renglon
                    if (verdadero === estado) {
                        return false;
                    }
                    return true;
                }
            );
            //Actualizamos la tabla
            tablaCompra.draw();
        } else {
            //Reseteamos los filtros
            $.fn.dataTable.ext.search = [];
            $.fn.dataTable.ext.search.pop();
            tablaCompra.draw();
            $('.selectCliente').val(null).trigger('change');
            $('input[name="filterRangoFechas"]').val('');
            fechaInicio = '';
            fechaFin = '';
        }
    });
    //Boton Resetear Filtros
    $('.btnResetFilters').on('click', function () {
        $.fn.dataTable.ext.search = [];
        $.fn.dataTable.ext.search.pop();
        tablaCompra.draw();
        $('.selectProveedor').val(null).trigger('change');
        //Limpiamos limpio el Filtro de Rango de Fechas
        $('input[name="filterRangoFechas"]').val('');
        fechaInicio = '';
        fechaFin = '';
        $('#excluirCanceladas').prop('checked', false);
    });
//------------------------------------GENERAR REPORTE----------------------------------------//
    //Boton Generar Reporte
    $('#reporteForm').on('submit', function (e) {
        e.preventDefault();
        var dataCompras = [];
        //Recorremos el listado del Datatables para pasar el detalle con LOS FILTROS APLICADOS
        $('#data').DataTable().rows({filter: 'applied'}).every(function (rowIdx, tableLoop, rowLoop) {
            var data = this.data();
            dataCompras.push(data);
        });
        for (var i = 0; i < dataCompras.length; i++) {
            dataCompras[i].fecha = moment(moment(dataCompras[i].fecha, 'YYYY-MM-DD')).format('DD-MM-YYYY');
        }
        //Asignamos las variables a la estructura
        reporte.items.cliente = $('select[name="selectProveedor"]').val();
        reporte.items.fechaDesde = fechaInicio;
        reporte.items.fechaHasta = fechaFin;
        reporte.items.excluirCanceladas = checkCanceladas;
        reporte.items.compras = dataCompras;
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
    document.getElementById("excluirCanceladas").checked = true;
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