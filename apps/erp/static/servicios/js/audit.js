var tablaServicios;
//Creamos variables auxiliares para el reporte
var fechaInicio = '';
var fechaFin = '';
var checkCanceladas = true;
//Creamos una estructura para el Reporte
var reporte = {
    items: {
        //Filtros
        servicio: '',
        accion: '',
        usuario: '',
        fechaDesde: '',
        fechaHasta: '',
        //detalle de compras
        servicios: [],
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
    tablaServicios = $('#data').DataTable({
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
            {"data": "history_type"},
            {"data": "history_user"},
            {"data": "history_id"}, //va duplicado algun campo por la botonera
        ],
        columnDefs: [
            {
                targets: [-6, -2],
                class: 'text-center',
            },
            {
                targets: [-5],
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
            //Agregamos al Select2 los Servicios que tenemos en el listado
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
                    $('.selectServicio').append(newOption).trigger('change');
                });
            });
            //Agregamos al Select2 las acciones que tenemos en el listado
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
                    $('.selectUsuario').append(newOption).trigger('change');
                });
            });
            //Actualizamos la tabla
            tablaServicios.draw();
        }
    });
    $('#data tbody')
        .on('click', 'a[rel="detalleMovimiento"]', function () {
            //Asignamos a una variable el renglon que necesitamos
            var tr = tablaServicios.cell($(this).closest('td, li')).index();
            renglon = tr.row;
            //Asignamos a una variable el movimiento en base al renglon
            var audit = tablaServicios.row(tr.row).data();
            //Realizamos el AJAX para buscar el DETALLE DE LA AUDITORIA
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'view_movimiento',
                    'pk': audit.history_id,
                },
                dataType: 'json',
                headers: {
                    'X-CSRFToken': csrftoken
                },
            }).done(function (data) {
                var dato = data[0];
                //Cargamos los datos del Servicio y mostramos en el modal con las modificaciones
                var descripcion = $('#modalDescripcion').val(dato.descripcion);
                var codigo = $('#modalCodigo').val(dato.codigo);
                var costo = $('#modalCosto').val(dato.costo);
                var iva = $('#modalTipoIva').val(dato.iva);
                var precioVenta = $('#modalPrecioVenta').val(dato.precioVenta);
                var esfuerzo = $('#modalEsfuerzo').val(dato.esfuerzo);
                var imagen = $('#modalImagen').val(dato.imagen);
                $('#modalCategoriaOld').val(dato.imagen);
                if (audit.history_type === '~') {
                    var descripcionOld = document.getElementById('modalDescripcionOld');
                    descripcionOld.innerHTML = dato.descripcionOld;
                    var codigoOld = document.getElementById('modalCodigoOld');
                    codigoOld.innerHTML = dato.codigoOld;
                    var costoOld = document.getElementById('modalCostoOld');
                    costoOld.innerHTML = dato.costoOld;
                    var ivaOld = document.getElementById('modalTipoIvaOld');
                    ivaOld.innerHTML = dato.ivaOld;
                    var precioVentaOld = document.getElementById('modalPrecioVentaOld');
                    precioVentaOld.innerHTML = dato.precioVentaOld;
                    var esfuerzoOld = document.getElementById('modalEsfuerzoOld');
                    esfuerzoOld.innerHTML = dato.esfuerzoOld;
                    var imagenOld = document.getElementById('modalImagenOld');
                    imagenOld.innerHTML = dato.imagenOld;
                    if (descripcion.val() !== descripcionOld.innerHTML) {
                        descripcionOld.innerHTML = 'Valor anterior: ' + descripcionOld.innerHTML
                        $("#modalDescripcionOld").removeAttr("hidden");
                    }
                    if (codigo.val() !== codigoOld.innerHTML) {
                        codigoOld.innerHTML = 'Valor anterior: ' + codigoOld.innerHTML
                        $("#modalCodigoOld").removeAttr("hidden");
                    }
                    if (costo.val() !== costoOld.innerHTML) {
                        costoOld.innerHTML = 'Valor anterior: ' + costoOld.innerHTML
                        $("#modalCostoOld").removeAttr("hidden");
                    }
                    if (iva.val() !== ivaOld.innerHTML) {
                        ivaOld.innerHTML = 'Valor anterior: ' + ivaOld.innerHTML
                        $("#modalIvaOld").removeAttr("hidden");
                    }
                    if (precioVenta.val() !== precioVentaOld.innerHTML) {
                        precioVentaOld.innerHTML = 'Valor anterior: ' + precioVentaOld.innerHTML
                        $("#modalPrecioVentaOld").removeAttr("hidden");
                    }
                     if (esfuerzo.val() !== esfuerzoOld.innerHTML) {
                        esfuerzoOld.innerHTML = 'Valor anterior: ' + esfuerzoOld.innerHTML
                        $("#modalEsfuerzoOld").removeAttr("hidden");
                    }
                    if (imagen.val() !== imagenOld.innerHTML) {
                        imagenOld.innerHTML = 'Valor anterior: ' + imagenOld.innerHTML
                        $("#modalImagenOld").removeAttr("hidden");
                    }
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
            }).always(function (data) {
            });
            $('#modalServicio').modal('show');
        });
    //Al cerrar el Modal de Movimiento reseteamos los valores del formulario
    $('#modalServicio').on('hidden.bs.modal', function (e) {
        //Reseteamos los input del Modal
        $('#formServicio').trigger('reset');
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
        tablaServicios.draw();
    });
    //Aplicamos Filtro de Servicios
    $('.selectServicio').on('change', function () {
        //Reseteamos los filtros
        $.fn.dataTable.ext.search = [];
        $.fn.dataTable.ext.search.pop();
        tablaServicios.draw();
        $('.selectUsuario').val(null).trigger('change');
        $('.selectAccion').val(null).trigger('change');
        //Limpiamos limpio el Filtro de Rango de Fechas
        $('input[name="filterRangoFechas"]').val('');
        fechaInicio = '';
        fechaFin = '';
        //Asignamos a una variabla el servicio del Select
        var servicio = $(this).val();
        if (servicio !== null && servicio !== '' && servicio !== undefined) {
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el servicio por cada renglon
                    var servicioTabla = (data[2].toString());
                    //Comparamos contra el renglon
                    if (servicio === servicioTabla) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaServicios.draw();
        }
    });
    //Aplicamos Filtro de Accion
    $('.selectAccion').on('change', function () {
        //Reseteamos los filtros
        // $.fn.dataTable.ext.search = [];
        // $.fn.dataTable.ext.search.pop();
        // tablaServicios.draw();
        //Asignamos a una variabla el usuario del Select
        var accion = $(this).val();
        if (accion !== null && accion !== '' && accion !== undefined) {
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el usuario por cada renglon
                    var accionTabla = (data[3].toString());
                    //Comparamos contra el renglon
                    if (accion === accionTabla) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaServicios.draw();
        }
    });
    //Aplicamos Filtro de Usuarios
    $('.selectUsuario').on('change', function () {
        //Reseteamos los filtros
        // $.fn.dataTable.ext.search = [];
        // $.fn.dataTable.ext.search.pop();
        // tablaServicios.draw();
        //Asignamos a una variabla el usuario del Select
        var usuario = $(this).val();
        if (usuario !== null && usuario !== '' && usuario !== undefined) {
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el usuario por cada renglon
                    var usuarioTabla = (data[4].toString());
                    //Comparamos contra el renglon
                    if (usuario === usuarioTabla) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaServicios.draw();
        }
    });

    //Boton Resetear Filtros
    $('.btnResetFilters').on('click', function () {
        $.fn.dataTable.ext.search = [];
        $.fn.dataTable.ext.search.pop();
        tablaServicios.draw();
        $('.selectServicio').val(null).trigger('change');
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
        reporte.items.servicio = $('select[name="selectServicio"]').val();
        reporte.items.accion = $('select[name="selectAccion"]').val();
        reporte.items.usuario = $('select[name="selectUsuario"]').val();
        reporte.items.fechaDesde = fechaInicio;
        reporte.items.fechaHasta = fechaFin;
        reporte.items.servicios = dataAuditoria;
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