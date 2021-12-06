var tablaProductos;
var tablaServicios;
var cantProductos = 0;
var cantServicios = 0;
//Creamos una variable para cargar el SELECT de Clientes y Modelos
var select_clientes = $('select[name="selectCliente"]');
var select_modelos = $('select[name="selectModelo"]');
//Creamos variables auxiliares para el reporte
var fechaInicio = '';
var fechaFin = '';
var checkCancelados = true;
var checkNoConfirmados = false;
//Creamos una estructura para el Reporte
var reporte = {
    items: {
        //Filtros
        cliente: '',
        modelo: '',
        fechaDesde: '',
        fechaHasta: '',
        excluirCancelados: '',
        excluirNoConfirmados: '',
        //detalle de presupuestos
        presupuestos: [],
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
    var tablaPresupuesto = $('#data').DataTable({
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
            {"data": "id"},
            {"data": "fecha"},
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
                targets: [-6],
                class: 'text-center',
                // orderable: false,
                render: function (data, type, row) {
                    return moment(moment(data, 'YYYY-MM-DD')).format('DD-MM-YYYY');
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
                    var buttons = '<a rel="detallePresupuesto" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i></a> ';
                    buttons += '<a href="/presupuestos/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    if (row.estado !== false && row.estado !== true) {
                        buttons += '<a href="/presupuestos/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/presupuestos/confirm/' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fas fa-check"></i></a> ';
                        buttons += '<a href="/presupuestos/delete/' + row.id + '/" id="' + row.id + '" onclick="btnEliminar(this.id, this.href)" class="btn btn-danger btn-xs btn-flat" data-toggle="modal" data-target="#deleteModal"><i class="fas fa-times"></i>';
                    }
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {
            //Agregamos al Select2 los clientes que tenemos en el listado
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
                    var newOption = new Option(d.toString(), d.toString(), false, false);
                    $('.selectCliente').append(newOption).trigger('change');
                });
            });
            //Agregamos al Select2 los modelos que tenemos en el listado
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
                column.data().unique().sort().each(function (d, j) {
                    var newOption = new Option(d.toString(), d.toString(), false, false);
                    $('.selectModelo').append(newOption).trigger('change');
                });
            });
            //Excluimos los cancelados
            var verdadero = ' CANCELADO';
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
            tablaPresupuesto.draw();
        }
    });

    $('#data tbody')
        .on('click', 'a[rel="detallePresupuesto"]', function () {
            //Seleccionamos el Presupuesto sobre la cual queremos traer el detalle
            var tr = tablaPresupuesto.cell($(this).closest('td, li')).index();
            var data = tablaPresupuesto.row(tr.row).data();

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
                fechaInicio = picker.startDate.format('DD-MM-YYYY');
                fechaFin = picker.endDate.format('DD-MM-YYYY');
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
        tablaPresupuesto.draw();
    });

    //Aplicamos Filtro de Clientes
    $('.selectCliente').on('change', function () {
        /*//Reseteamos los filtros
        $.fn.dataTable.ext.search = [];
        $.fn.dataTable.ext.search.pop();
        tablaPresupuesto.draw();*/
        //Asignamos a una variabla el cliente del Select
        var cliente = $(this).val();
        if (cliente !== null && cliente !== '' && cliente !== undefined) {
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el cliente por cada renglon
                    var clienteTabla = (data[5].toString());
                    //Comparamos contra el renglon
                    if (cliente === clienteTabla) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaPresupuesto.draw();
        }
    });
    //Aplicamos Filtro de Modelos
    $('.selectModelo').on('change', function () {
        /*//Reseteamos los filtros
        $.fn.dataTable.ext.search = [];
        $.fn.dataTable.ext.search.pop();
        tablaPresupuesto.draw();*/
        //Asignamos a una variabla el cliente del Select
        var modelo = $(this).val();
        if (modelo !== null && modelo !== '' && modelo !== undefined) {
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el cliente por cada renglon
                    var modeloTabla = (data[4].toString());
                    //Comparamos contra el renglon
                    if (modelo === modeloTabla) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaPresupuesto.draw();
        }
    });
    //Filtrar Trabajos Asociados
    $('#excluirNoConfirmados').on('click', function () {
        var verdadero = ' NO CONFIRMADO';
        if (this.checked) {
            //Asignamos Verdadero a la variable auxiliar del reporte
            checkNoConfirmados = true;
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
            tablaPresupuesto.draw();
        } else {
            //Reseteamos los filtros
            checkNoConfirmados = false;
            $.fn.dataTable.ext.search = [];
            $.fn.dataTable.ext.search.pop();
            tablaPresupuesto.draw();
            document.getElementById("excluirCancelados").checked = false;
            $('.selectCliente').val(null).trigger('change');
            $('.selectModelo').val(null).trigger('change');
            $('input[name="filterRangoFechas"]').val('');
            fechaInicio = '';
            fechaFin = '';
        }
    });
    //Filtrar Estado Cancelados
    $('#excluirCancelados').on('click', function () {
        var verdadero = ' CANCELADO';
        if (this.checked) {
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
            tablaPresupuesto.draw();
        } else {
            //Reseteamos los filtros
            checkCancelados = false;
            $.fn.dataTable.ext.search = [];
            $.fn.dataTable.ext.search.pop();
            tablaPresupuesto.draw();
            document.getElementById("excluirNoConfirmados").checked = false;
            $('.selectCliente').val(null).trigger('change');
            $('.selectModelo').val(null).trigger('change');
            $('input[name="filterRangoFechas"]').val('');
            fechaInicio = '';
            fechaFin = '';
        }
    });

    //Boton Resetear Filtros
    $('.btnResetFilters').on('click', function () {
        $.fn.dataTable.ext.search = [];
        $.fn.dataTable.ext.search.pop();
        tablaPresupuesto.draw();
        $('.selectCliente').val(null).trigger('change');
        $('.selectModelo').val(null).trigger('change');
        //Limpiamos limpio el Filtro de Rango de Fechas
        $('input[name="filterRangoFechas"]').val('');
        fechaInicio = '';
        fechaFin = '';
        $('#excluirNoConfirmados').prop('checked', false);
        $('#excluirCancelados').prop('checked', false);
    });
//------------------------------------GENERAR REPORTE----------------------------------------//
    //Boton Generar Reporte
    $('#reporteForm').on('submit', function (e) {
        e.preventDefault();
        var dataPresupuestos = [];
        //Recorremos el listado del Datatables para pasar el detalle con LOS FILTROS APLICADOS
        $('#data').DataTable().rows({filter: 'applied'}).every(function (rowIdx, tableLoop, rowLoop) {
            var data = this.data();
            dataPresupuestos.push(data);
        });
        //Damos formato a la fecha para visualizar correctamente
        for (var i = 0; i < dataPresupuestos.length; i++) {
            dataPresupuestos[i].fecha = moment(moment(dataPresupuestos[i].fecha, 'YYYY-MM-DD')).format('DD-MM-YYYY');
        }
        //Asignamos las variables a la estructura
        reporte.items.cliente = $('select[name="selectCliente"]').val();
        reporte.items.fechaDesde = fechaInicio;
        reporte.items.fechaHasta = fechaFin;
        reporte.items.excluirCancelados = checkCancelados;
        reporte.items.excluirNoConfirmados = checkNoConfirmados;
        reporte.items.presupuestos = dataPresupuestos;
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
    document.getElementById("excluirNoConfirmados").checked = false;
    document.getElementById("excluirCancelados").checked = true;
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