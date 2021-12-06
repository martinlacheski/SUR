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
        accion: '',
        usuario: '',
        fechaDesde: '',
        fechaHasta: '',
        //detalle de compras
        productos: [],
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
            tablaProductos.draw();
        }
    });
    $('#data tbody')
        .on('click', 'a[rel="detalleMovimiento"]', function () {
            //Asignamos a una variable el renglon que necesitamos
            var tr = tablaProductos.cell($(this).closest('td, li')).index();
            renglon = tr.row;
            //Asignamos a una variable el movimiento en base al renglon
            var audit = tablaProductos.row(tr.row).data();
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
                //Cargamos los datos del Producto y mostramos en el modal con las modificaciones
                var categoria = $('#modalCategoria').val(dato.categoria);
                var subcategoria = $('#modalSubcategoria').val(dato.subcategoria);
                var descripcion = $('#modalDescripcion').val(dato.descripcion);
                var abreviatura = $('#modalAbreviatura').val(dato.abreviatura);
                var codigo = $('#modalCodigo').val(dato.codigo);
                var codigoProveedor = $('#modalCodigoProveedor').val(dato.codigoProveedor);
                var codigoBarras1 = $('#modalCodigoBarras1').val(dato.codigoBarras1);
                var stockReal = $('#modalStockReal').val(dato.stockReal);
                var stockMinimo = $('#modalStockMinimo').val(dato.stockMinimo);
                var reposicion = $('#modalReposicion').val(dato.reposicion);
                var costo = $('#modalCosto').val(dato.costo);
                var utilidad = $('#modalUtilidad').val(dato.utilidad);
                var iva = $('#modalTipoIva').val(dato.iva);
                var precioVenta = $('#modalPrecioVenta').val(dato.precioVenta);
                var ubicacion = $('#modalUbicacion').val(dato.ubicacion);
                var observaciones = $('#modalObservaciones').val(dato.observaciones);
                var esInsumo = $('#modalEsInsumo').val(dato.esInsumo);
                var descuentaStock = $('#modalDescuentaStock').val(dato.descuentaStock);
                var imagen = $('#modalImagen').val(dato.imagen);
                $('#modalCategoriaOld').val(dato.imagen);
                if (audit.history_type === '~') {
                    var categoriaOld = document.getElementById('modalCategoriaOld');
                    categoriaOld.innerHTML = dato.categoriaOld;
                    var subcategoriaOld = document.getElementById('modalSubcategoriaOld');
                    subcategoriaOld.innerHTML = dato.subcategoriaOld;
                    var descripcionOld = document.getElementById('modalDescripcionOld');
                    descripcionOld.innerHTML = dato.descripcionOld;
                    var abreviaturaOld = document.getElementById('modalAbreviaturaOld');
                    abreviaturaOld.innerHTML = dato.abreviaturaOld;
                    var codigoOld = document.getElementById('modalCodigoOld');
                    codigoOld.innerHTML = dato.codigoOld;
                    var codigoProveedorOld = document.getElementById('modalCodigoProveedorOld');
                    codigoProveedorOld.innerHTML = dato.codigoProveedorOld;
                    var codigoBarras1Old = document.getElementById('modalCodigoBarras1Old');
                    codigoBarras1Old.innerHTML = dato.codigoBarras1Old;
                    var stockRealOld = document.getElementById('modalStockRealOld');
                    stockRealOld.innerHTML = dato.stockRealOld;
                    var stockMinimoOld = document.getElementById('modalStockMinimoOld');
                    stockMinimoOld.innerHTML = dato.stockMinimoOld;
                    var reposicionOld = document.getElementById('modalReposicionOld');
                    reposicionOld.innerHTML = dato.reposicionOld;
                    var costoOld = document.getElementById('modalCostoOld');
                    costoOld.innerHTML = dato.costoOld;
                    var utilidadOld = document.getElementById('modalUtilidadOld');
                    utilidadOld.innerHTML = dato.utilidadOld;
                    var ivaOld = document.getElementById('modalTipoIvaOld');
                    ivaOld.innerHTML = dato.ivaOld;
                    var precioVentaOld = document.getElementById('modalPrecioVentaOld');
                    precioVentaOld.innerHTML = dato.precioVentaOld;
                    var ubicacionOld = document.getElementById('modalUbicacionOld');
                    ubicacionOld.innerHTML = dato.ubicacionOld;
                    var observacionesOld = document.getElementById('modalObservacionesOld');
                    observacionesOld.innerHTML = dato.observacionesOld;
                    var esInsumoOld = document.getElementById('modalEsInsumoOld');
                    esInsumoOld.innerHTML = dato.esInsumoOld;
                    var descuentaStockOld = document.getElementById('modalDescuentaStockOld');
                    descuentaStockOld.innerHTML = dato.descuentaStockOld;
                    var imagenOld = document.getElementById('modalImagenOld');
                    imagenOld.innerHTML = dato.imagenOld;
                    if (categoria.val() !== categoriaOld.innerHTML) {
                        categoriaOld.innerHTML = 'Valor anterior: ' + categoriaOld.innerHTML
                        $("#modalCategoriaOld").removeAttr("hidden");
                    }
                    if (subcategoria.val() !== subcategoriaOld.innerHTML) {
                        subcategoriaOld.innerHTML = 'Valor anterior: ' + subcategoriaOld.innerHTML
                        $("#modalSubcategoriaOld").removeAttr("hidden");
                    }
                    if (descripcion.val() !== descripcionOld.innerHTML) {
                        descripcionOld.innerHTML = 'Valor anterior: ' + descripcionOld.innerHTML
                        $("#modalDescripcionOld").removeAttr("hidden");
                    }
                    if (abreviatura.val() !== abreviaturaOld.innerHTML) {
                        abreviaturaOld.innerHTML = 'Valor anterior: ' + abreviaturaOld.innerHTML
                        $("#modalAbreviaturaOld").removeAttr("hidden");
                    }
                    if (codigo.val() !== codigoOld.innerHTML) {
                        codigoOld.innerHTML = 'Valor anterior: ' + codigoOld.innerHTML
                        $("#modalCodigoOld").removeAttr("hidden");
                    }
                    if (codigoProveedor.val() !== codigoProveedorOld.innerHTML) {
                        codigoProveedorOld.innerHTML = 'Valor anterior: ' + codigoProveedorOld.innerHTML
                        $("#modalCodigoProveedorOld").removeAttr("hidden");
                    }
                    if (codigoBarras1.val() !== codigoBarras1Old.innerHTML) {
                        codigoBarras1Old.innerHTML = 'Valor anterior: ' + codigoBarras1Old.innerHTML
                        $("#modalCodigoBarras1Old").removeAttr("hidden");
                    }
                    if (stockReal.val() !== stockRealOld.innerHTML) {
                        stockRealOld.innerHTML = 'Valor anterior: ' + stockRealOld.innerHTML
                        $("#modalStockRealOld").removeAttr("hidden");
                    }
                    if (stockMinimo.val() !== stockMinimoOld.innerHTML) {
                        stockMinimoOld.innerHTML = 'Valor anterior: ' + stockMinimoOld.innerHTML
                        $("#modalStockMinimoOld").removeAttr("hidden");
                    }
                    if (reposicion.val() !== reposicionOld.innerHTML) {
                        reposicionOld.innerHTML = 'Valor anterior: ' + reposicionOld.innerHTML
                        $("#modalReposicionOld").removeAttr("hidden");
                    }
                    if (costo.val() !== costoOld.innerHTML) {
                        costoOld.innerHTML = 'Valor anterior: ' + costoOld.innerHTML
                        $("#modalCostoOld").removeAttr("hidden");
                    }
                    if (utilidad.val() !== utilidadOld.innerHTML) {
                        utilidadOld.innerHTML = 'Valor anterior: ' + utilidadOld.innerHTML
                        $("#modalUtilidadOld").removeAttr("hidden");
                    }
                    if (iva.val() !== ivaOld.innerHTML) {
                        ivaOld.innerHTML = 'Valor anterior: ' + ivaOld.innerHTML
                        $("#modalIvaOld").removeAttr("hidden");
                    }
                    if (precioVenta.val() !== precioVentaOld.innerHTML) {
                        precioVentaOld.innerHTML = 'Valor anterior: ' + precioVentaOld.innerHTML
                        $("#modalPrecioVentaOld").removeAttr("hidden");
                    }
                    if (ubicacion.val() !== ubicacionOld.innerHTML) {
                        ubicacionOld.innerHTML = 'Valor anterior: ' + ubicacionOld.innerHTML
                        $("#modalUbicacionOld").removeAttr("hidden");
                    }
                    if (observaciones.val() !== observacionesOld.innerHTML) {
                        observacionesOld.innerHTML = 'Valor anterior: ' + observacionesOld.innerHTML
                        $("#modalObservacionesOld").removeAttr("hidden");
                    }
                    if (esInsumo.val() !== esInsumoOld.innerHTML) {
                        esInsumoOld.innerHTML = 'Valor anterior: ' + esInsumoOld.innerHTML
                        $("#modalEsInsumoOld").removeAttr("hidden");
                    }
                    if (descuentaStock.val() !== descuentaStockOld.innerHTML) {
                        descuentaStockOld.innerHTML = 'Valor anterior: ' + descuentaStockOld.innerHTML
                        $("#modalDescuentaStockOld").removeAttr("hidden");
                    }
                    if (imagen.val() !== imagenOld.innerHTML) {
                        imagenOld.innerHTML = 'Valor anterior: ' + imagenOld.innerHTML
                        $("#modalImagenOld").removeAttr("hidden");
                    }
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
            }).always(function (data) {
            });
            $('#modalProducto').modal('show');
        });
    //Al cerrar el Modal de Movimiento reseteamos los valores del formulario
    $('#modalProducto').on('hidden.bs.modal', function (e) {
        //Reseteamos los input del Modal
        $('#formProducto').trigger('reset');
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
    //Aplicamos Filtro de Accion
    $('.selectAccion').on('change', function () {
        //Reseteamos los filtros
        $.fn.dataTable.ext.search = [];
        $.fn.dataTable.ext.search.pop();
        tablaProductos.draw();
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
                    var usuarioTabla = (data[4].toString());
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
        reporte.items.producto = $('select[name="selectProducto"]').val();
        reporte.items.accion = $('select[name="selectAccion"]').val();
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