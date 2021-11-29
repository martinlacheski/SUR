var tablaProductos;
var tablaServicios;
var cantProductos = 0;
var cantServicios = 0;
var estadoInicial = 0;
var estadoPlanificado = 0;
var estadoEspecial = 0;
var estadoFinalizado = 0;
var estadoEntregado = 0;
var estadoCancelado = 0;
//Creamos una variable para cargar el SELECT de Clientes y Modelos
var select_clientes = $('select[name="selectCliente"]');
var select_modelos = $('select[name="selectModelo"]');
//Creamos variables auxiliares para el reporte
var fechaInicio = '';
var fechaFin = '';
var checkPendientes = false;
var checkPlanificados = false;
var checkEnProceso = false;
var checkFinalizados = false;
var checkCancelados = true;
var checkEntregados = false;
//Creamos una estructura para el Reporte
var reporte = {
    items: {
        //Filtros
        cliente: '',
        modelo: '',
        usuarioAsignado: '',
        fechaDesde: '',
        fechaHasta: '',
        excluirEntregados: '',
        excluirCancelados: '',
        verPendientes: '',
        verPlanificados: '',
        verEnProceso: '',
        verFinalizados: '',
        //detalle de trabajos
        trabajos: [],
    },
};

//Funcion para buscar los parametros de estado
function searchParametros() {
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrftoken,
            'action': 'get_parametros_estados',
        },
        dataType: 'json',
        success: function (data) {
            estadoInicial = data[0].estadoInicial.id;
            estadoPlanificado = data[0].estadoPlanificado.id;
            estadoEspecial = data[0].estadoEspecial.id;
            estadoFinalizado = data[0].estadoFinalizado.id;
            estadoEntregado = data[0].estadoEntregado.id;
            estadoCancelado = data[0].estadoCancelado.id;
        }
    });
};

$(function () {
    //Buscamos los parametros de estado
    searchParametros();
    //Eventos del Listado
    var tablaTrabajo = $('#data').DataTable({
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
            {"data": "estadoTrabajo.nombre"},
            {"data": "porcentaje"},
            {"data": "fechaEntrada"},
            {"data": "fechaSalida"},
            {"data": "modelo.nombre"},
            {"data": "cliente.razonSocial"},
            {"data": "asignado"}, //Duplicado para ver el Usuario Asignado
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
                    if (row.estadoTrabajo.id == estadoInicial) {
                        return '<span class="badge badge-warning">' + row.estadoTrabajo.nombre + '</span>'
                    } else if (row.estadoTrabajo.id == estadoPlanificado) {
                        return '<span class="badge badge-dark">' + row.estadoTrabajo.nombre + '</span>'
                    } else if (row.estadoTrabajo.id == estadoEspecial) {
                        return '<span class="badge badge-info">' + row.estadoTrabajo.nombre + '</span>'
                    } else if (row.estadoTrabajo.id == estadoFinalizado) {
                        return '<span class="badge badge-success">' + row.estadoTrabajo.nombre + '</span>'
                    } else if (row.estadoTrabajo.id == estadoCancelado) {
                        return '<span class="badge badge-danger">' + row.estadoTrabajo.nombre + '</span>'
                    } else if (row.estadoTrabajo.id == estadoEntregado) {
                        return '<span class="badge badge-primary">' + row.estadoTrabajo.nombre + '</span>'
                    } else {
                        return '<span class="badge badge-info">' + row.estadoTrabajo.nombre + '</span>'
                    }
                }
            },
            {
                targets: [-7],
                class: 'text-center',
                render: function (data, type, row) {
                    var porcentaje = parseFloat(row.porcentaje).toFixed(2);
                    if (porcentaje <= 24.99) {
                        return '<span class="badge badge-danger">' + porcentaje + '</span>'
                    } else if (porcentaje >= 25 & porcentaje <= 49.99) {
                        return '<span class="badge badge-warning">' + porcentaje + '</span>'
                    } else if (porcentaje >= 50 & porcentaje <= 74.99) {
                        return '<span class="badge badge-info">' + porcentaje + '</span>'
                    } else if (porcentaje >= 75 & porcentaje <= 99.99) {
                        return '<span class="badge badge-success">' + porcentaje + '</span>'
                    } else {
                        return '<span class="badge badge-primary">' + porcentaje + '</span>'
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
                targets: [-5],
                class: 'text-center',
                // orderable: false,
                render: function (data, type, row) {
                    if (row.fechaSalida) {
                        return moment(moment(data, 'YYYY-MM-DD')).format('DD-MM-YYYY');
                    } else {
                        return '<span class="badge badge-danger">' + ' PENDIENTE' + '</span>'
                    }
                }
            },
            {
                targets: [-3, -4],
                class: 'text-center',
                orderable: false,
            },
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    if (row.asignado !== 'EXPRESS') {
                        return row.asignado
                    } else {
                        return '<span class="badge badge-success">' + row.asignado + '</span>'
                    }
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (!row.fechaSalida && row.estadoTrabajo.id !== estadoFinalizado) {
                        var buttons = '<a rel="detalleTrabajo" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i></a> ';
                        buttons += '<a href="/trabajos/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                        buttons += '<a href="/trabajos/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/trabajos/confirm/' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fas fa-check"></i></a> ';
                        buttons += '<a href="/trabajos/deliver/' + row.id + '/" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-people-carry"></i></a> ';
                        buttons += '<a href="/trabajos/delete/' + row.id + '/" id="' + row.id + '" onclick="btnEliminar(this.id, this.href)" class="btn btn-danger btn-xs btn-flat" data-toggle="modal" data-target="#deleteModal"><i class="fas fa-times"></i>';
                    } else if (row.estadoTrabajo.id == estadoFinalizado) {
                        var buttons = '<a rel="detalleTrabajo" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i></a> ';
                        buttons += '<a href="/trabajos/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                        buttons += '<a href="/trabajos/deliver/' + row.id + '/" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-people-carry"></i></a> ';
                    } else if (row.estadoTrabajo.id == estadoCancelado) {
                        var buttons = '<a rel="detalleTrabajo" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i></a> ';
                        buttons += '<a href="/trabajos/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    } else if (row.estadoTrabajo.id == estadoEntregado) {
                        var buttons = '<a rel="detalleTrabajo" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i></a> ';
                        buttons += '<a href="/trabajos/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    } else {
                        var buttons = '<a rel="detalleTrabajo" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i></a> ';
                        buttons += '<a href="/trabajos/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                        buttons += '<a href="/trabajos/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/trabajos/confirm/' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fas fa-check"></i></a> ';
                        buttons += '<a href="/trabajos/deliver/' + row.id + '/" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-people-carry"></i></a> ';
                        buttons += '<a href="/trabajos/delete/' + row.id + '/" id="' + row.id + '" onclick="btnEliminar(this.id, this.href)" class="btn btn-danger btn-xs btn-flat" data-toggle="modal" data-target="#deleteModal"><i class="fas fa-times"></i>';
                    }
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {
            //Agregamos al Select2 los clientes que tenemos en el listado
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
                    $('.selectCliente').append(newOption).trigger('change');
                });
            });
            //Agregamos al Select2 los modelos que tenemos en el listado
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
                    try {
                        var newOption = new Option(d.toString(), d.toString(), false, false);
                        $('.selectModelo').append(newOption).trigger('change');
                    } catch (error) {

                    }

                });
            });
            //Agregamos al Select2 los usuarios Asignados que tenemos en el listado
            this.api().columns(7).every(function () {
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
                    try {
                        var newOption = new Option(d.toString(), d.toString(), false, false);
                        $('.selectUsuario').append(newOption).trigger('change');
                    } catch (error) {

                    }

                });
            });
            //Excluimos los cancelados
            var verdadero = 'CANCELADO';
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
            tablaTrabajo.draw();
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
                    {"data": "estado"},
                    {"data": "precio"},
                    {"data": "cantidad"},
                    {"data": "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [-4],
                        class: 'text-center',
                        className: 'dt-body-center',
                        render: function (data, type, row) {
                            if (row.estado) {
                                return '<span class="badge badge-success">' + ' REALIZADO' + '</span>'
                            } else {
                                return '<span class="badge badge-danger">' + ' PENDIENTE' + '</span>'
                            }
                        }
                    },
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
                    {"data": "estado"},
                    {"data": "precio"},
                    {"data": "cantidad"},
                    {"data": "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [-4],
                        class: 'text-center',
                        className: 'dt-body-center',
                        render: function (data, type, row) {
                            if (row.estado) {
                                return '<span class="badge badge-success">' + ' REALIZADO' + '</span>'
                            } else {
                                return '<span class="badge badge-danger">' + ' PENDIENTE' + '</span>'
                            }
                        }
                    },
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
            document.getElementById("filters1").style.display = "";
            document.getElementById("filters2").style.display = "";
            document.getElementById("filters3").style.display = "";
        } else {
            document.getElementById("filters").style.display = "none";
            document.getElementById("filters1").style.display = "none";
            document.getElementById("filters2").style.display = "none";
            document.getElementById("filters3").style.display = "none";
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
                var dia = moment(moment(data[3], 'DD-MM-YYYY')).format('YYYY-MM-DD');
                //Comparamos contra el renglon
                if (desde <= dia && dia <= hasta) {
                    return true;
                }
                return false;
            }
        );
        //Actualizamos la tabla
        tablaTrabajo.draw();
    });

    //Aplicamos Filtro de Clientes
    $('.selectCliente').on('change', function () {
        //Reseteamos los filtros
        $.fn.dataTable.ext.search = [];
        $.fn.dataTable.ext.search.pop();
        tablaTrabajo.draw();
        //Asignamos a una variabla el cliente del Select
        var cliente = $(this).val();
        if (cliente !== null && cliente !== '' && cliente !== undefined) {
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el cliente por cada renglon
                    var clienteTabla = (data[6].toString());
                    //Comparamos contra el renglon
                    if (cliente === clienteTabla) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaTrabajo.draw();
        }
    });
    //Aplicamos Filtro de Modelos
    $('.selectModelo').on('change', function () {
        // //Reseteamos los filtros
        // $.fn.dataTable.ext.search = [];
        // $.fn.dataTable.ext.search.pop();
        // tablaTrabajo.draw();
        //Asignamos a una variabla el cliente del Select
        var modelo = $(this).val();
        if (modelo !== null && modelo !== '' && modelo !== undefined) {
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el cliente por cada renglon
                    var modeloTabla = (data[5].toString());
                    //Comparamos contra el renglon
                    if (modelo === modeloTabla) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaTrabajo.draw();
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
                    var usuarioTabla = (data[7].toString());
                    //Comparamos contra el renglon
                    if (usuario === usuarioTabla) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaTrabajo.draw();
        }
    });
    //Excluir Estado Finalizados
    $('#excluirFinalizados').on('click', function () {
        var verdadero = 'FINALIZADO';
        if (this.checked) {
            //Asignamos Verdadero a la variable auxiliar del reporte
            checkFinalizados = true;
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
            tablaTrabajo.draw();
        } else {
            //Reseteamos los filtros
            checkFinalizados = false;
            $.fn.dataTable.ext.search = [];
            $.fn.dataTable.ext.search.pop();
            tablaTrabajo.draw();
            document.getElementById("verPendientes").checked = false;
            document.getElementById("verPlanificados").checked = false;
            document.getElementById("verEnProceso").checked = false;
            document.getElementById("verFinalizados").checked = false;
            $('.selectCliente').val(null).trigger('change');
            $('.selectModelo').val(null).trigger('change');
            $('input[name="filterRangoFechas"]').val('');
            fechaInicio = '';
            fechaFin = '';
        }
    });
    //Excluir Estado Entregados
    $('#excluirEntregados').on('click', function () {
        var verdadero = 'ENTREGADO';
        if (this.checked) {
            //Asignamos Verdadero a la variable auxiliar del reporte
            checkEntregados = true;
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
            tablaTrabajo.draw();
        } else {
            //Reseteamos los filtros
            checkEntregados = false;
            $.fn.dataTable.ext.search = [];
            $.fn.dataTable.ext.search.pop();
            tablaTrabajo.draw();
            document.getElementById("verPendientes").checked = false;
            document.getElementById("verPlanificados").checked = false;
            document.getElementById("verEnProceso").checked = false;
            document.getElementById("verFinalizados").checked = false;
            $('.selectCliente').val(null).trigger('change');
            $('.selectModelo').val(null).trigger('change');
            $('input[name="filterRangoFechas"]').val('');
            fechaInicio = '';
            fechaFin = '';
        }
    });
    //Excluir Estado Cancelados
    $('#excluirCancelados').on('click', function () {
        var verdadero = 'CANCELADO';
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
            tablaTrabajo.draw();
        } else {
            //Reseteamos los filtros
            checkCancelados = false;
            $.fn.dataTable.ext.search = [];
            $.fn.dataTable.ext.search.pop();
            tablaTrabajo.draw();
            document.getElementById("verPendientes").checked = false;
            document.getElementById("verPlanificados").checked = false;
            document.getElementById("verEnProceso").checked = false;
            document.getElementById("verFinalizados").checked = false;
            $('.selectCliente').val(null).trigger('change');
            $('.selectModelo').val(null).trigger('change');
            $('input[name="filterRangoFechas"]').val('');
            fechaInicio = '';
            fechaFin = '';
        }
    });
    //Ver Estado Pendientes
    $('#verPendientes').on('click', function () {
        var verdadero = 'PENDIENTE';
        if (this.checked) {
            //Cambiamos el CHECK de los otros estados determinados
            document.getElementById("excluirFinalizados").checked = false;
            document.getElementById("excluirEntregados").checked = false;
            document.getElementById("verPlanificados").checked = false;
            document.getElementById("verEnProceso").checked = false;
            document.getElementById("verFinalizados").checked = false;
            //Reseteamos Cliente y Modelo
            $('.selectCliente').val(null).trigger('change');
            $('.selectModelo').val(null).trigger('change');
            //Reseteamos la Tabla
            $.fn.dataTable.ext.search = [];
            $.fn.dataTable.ext.search.pop();
            tablaTrabajo.draw();
            //Asignamos Verdadero a la variable auxiliar del reporte
            checkPendientes = true;
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el estado por cada renglon
                    var estado = (data[1]);
                    //Comparamos contra el renglon
                    if (verdadero === estado) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaTrabajo.draw();
        } else {
            //Reseteamos los filtros
            checkPendientes = false;
            //Reseteamos Cliente y Modelo
            $('.selectCliente').val(null).trigger('change');
            $('.selectModelo').val(null).trigger('change');
            //Reseteamos la Tabla
            $.fn.dataTable.ext.search = [];
            $.fn.dataTable.ext.search.pop();
            tablaTrabajo.draw();
            document.getElementById("excluirEntregados").checked = false;
            document.getElementById("excluirCancelados").checked = false;
            document.getElementById("verPendientes").checked = false;
            document.getElementById("verPlanificados").checked = false;
            document.getElementById("verEnProceso").checked = false;
            document.getElementById("verFinalizados").checked = false;
            $('.selectCliente').val(null).trigger('change');
            $('.selectModelo').val(null).trigger('change');
            $('input[name="filterRangoFechas"]').val('');
            fechaInicio = '';
            fechaFin = '';
        }
    });
    //Ver Estado Planificados
    $('#verPlanificados').on('click', function () {
        var verdadero = 'PLANIFICADO';
        if (this.checked) {
            //Cambiamos el CHECK de los otros estados determinados
            document.getElementById("excluirFinalizados").checked = false;
            document.getElementById("excluirEntregados").checked = false;
            document.getElementById("verPendientes").checked = false;
            document.getElementById("verEnProceso").checked = false;
            document.getElementById("verFinalizados").checked = false;
            //Reseteamos Cliente y Modelo
            $('.selectCliente').val(null).trigger('change');
            $('.selectModelo').val(null).trigger('change');
            //Reseteamos la Tabla
            $.fn.dataTable.ext.search = [];
            $.fn.dataTable.ext.search.pop();
            tablaTrabajo.draw();
            //Asignamos Verdadero a la variable auxiliar del reporte
            checkPlanificados = true;
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el estado por cada renglon
                    var estado = (data[1]);
                    //Comparamos contra el renglon
                    if (verdadero === estado) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaTrabajo.draw();
        } else {
            //Reseteamos los filtros
            checkPlanificados = false;
            //Reseteamos Cliente y Modelo
            $('.selectCliente').val(null).trigger('change');
            $('.selectModelo').val(null).trigger('change');
            //Reseteamos la Tabla
            $.fn.dataTable.ext.search = [];
            $.fn.dataTable.ext.search.pop();
            tablaTrabajo.draw();
            document.getElementById("excluirEntregados").checked = false;
            document.getElementById("excluirCancelados").checked = false;
            document.getElementById("verPendientes").checked = false;
            document.getElementById("verPlanificados").checked = false;
            document.getElementById("verEnProceso").checked = false;
            document.getElementById("verFinalizados").checked = false;
            $('.selectCliente').val(null).trigger('change');
            $('.selectModelo').val(null).trigger('change');
            $('input[name="filterRangoFechas"]').val('');
            fechaInicio = '';
            fechaFin = '';
        }
    });
    //Ver Estado En Proceso
    $('#verEnProceso').on('click', function () {
        var verdadero = 'EN PROCESO';
        if (this.checked) {
            //Cambiamos el CHECK de los otros estados determinados
            document.getElementById("excluirFinalizados").checked = false;
            document.getElementById("excluirEntregados").checked = false;
            document.getElementById("verPendientes").checked = false;
            document.getElementById("verPlanificados").checked = false;
            document.getElementById("verFinalizados").checked = false;
            //Reseteamos Cliente y Modelo
            $('.selectCliente').val(null).trigger('change');
            $('.selectModelo').val(null).trigger('change');
            //Reseteamos la Tabla
            $.fn.dataTable.ext.search = [];
            $.fn.dataTable.ext.search.pop();
            tablaTrabajo.draw();
            //Asignamos Verdadero a la variable auxiliar del reporte
            verEnProceso = true;
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el estado por cada renglon
                    var estado = (data[1]);
                    //Comparamos contra el renglon
                    if (verdadero === estado) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaTrabajo.draw();
        } else {
            //Reseteamos los filtros
            verEnProceso = false;
            //Reseteamos Cliente y Modelo
            $('.selectCliente').val(null).trigger('change');
            $('.selectModelo').val(null).trigger('change');
            //Reseteamos la Tabla
            $.fn.dataTable.ext.search = [];
            $.fn.dataTable.ext.search.pop();
            tablaTrabajo.draw();
            document.getElementById("excluirEntregados").checked = false;
            document.getElementById("excluirCancelados").checked = false;
            document.getElementById("verPendientes").checked = false;
            document.getElementById("verPlanificados").checked = false;
            document.getElementById("verEnProceso").checked = false;
            document.getElementById("verFinalizados").checked = false;
            $('.selectCliente').val(null).trigger('change');
            $('.selectModelo').val(null).trigger('change');
            $('input[name="filterRangoFechas"]').val('');
            fechaInicio = '';
            fechaFin = '';
        }
    });
    //Ver Estado Finalizados
    $('#verFinalizados').on('click', function () {
        var verdadero = 'FINALIZADO';
        if (this.checked) {
            //Cambiamos el CHECK de los otros estados determinados
            document.getElementById("verPendientes").checked = false;
            document.getElementById("verPlanificados").checked = false;
            document.getElementById("verEnProceso").checked = false;
            //Reseteamos Cliente y Modelo
            $('.selectCliente').val(null).trigger('change');
            $('.selectModelo').val(null).trigger('change');
            //Reseteamos la Tabla
            $.fn.dataTable.ext.search = [];
            $.fn.dataTable.ext.search.pop();
            tablaTrabajo.draw();
            //Asignamos Verdadero a la variable auxiliar del reporte
            verFinalizados = true;
            //Extendemos la busqueda del datatables
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    // Asignamos el estado por cada renglon
                    var estado = (data[1]);
                    //Comparamos contra el renglon
                    if (verdadero === estado) {
                        return true;
                    }
                    return false;
                }
            );
            //Actualizamos la tabla
            tablaTrabajo.draw();
        } else {
            //Reseteamos los filtros
            verFinalizados = false;
            //Reseteamos Cliente y Modelo
            $('.selectCliente').val(null).trigger('change');
            $('.selectModelo').val(null).trigger('change');
            //Reseteamos la Tabla
            $.fn.dataTable.ext.search = [];
            $.fn.dataTable.ext.search.pop();
            tablaTrabajo.draw();
            document.getElementById("excluirEntregados").checked = false;
            document.getElementById("excluirCancelados").checked = false;
            document.getElementById("verPendientes").checked = false;
            document.getElementById("verPlanificados").checked = false;
            document.getElementById("verEnProceso").checked = false;
            document.getElementById("verFinalizados").checked = false;
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
        tablaTrabajo.draw();
        $('.selectCliente').val(null).trigger('change');
        $('.selectModelo').val(null).trigger('change');
        $('.selectUsuario').val(null).trigger('change');
        //Limpiamos limpio el Filtro de Rango de Fechas
        $('input[name="filterRangoFechas"]').val('');
        fechaInicio = '';
        fechaFin = '';
        $('#excluirFinalizados').prop('checked', false);
        $('#excluirEntregados').prop('checked', false);
        $('#excluirCancelados').prop('checked', true);
        $('#verPendientes').prop('checked', false);
        $('#verPlanificados').prop('checked', false);
        $('#verEnProceso').prop('checked', false);
        $('#verFinalizados').prop('checked', false);
    });
//------------------------------------GENERAR REPORTE----------------------------------------//
    //Boton Generar Reporte
    $('#reporteForm').on('submit', function (e) {
        e.preventDefault();
        var dataTrabajos = [];
        //Recorremos el listado del Datatables para pasar el detalle con LOS FILTROS APLICADOS
        $('#data').DataTable().rows({filter: 'applied'}).every(function (rowIdx, tableLoop, rowLoop) {
            var data = this.data();
            dataTrabajos.push(data);
        });
        //Damos formato a la fecha para visualizar correctamente
        for (var i = 0; i < dataTrabajos.length; i++) {
            dataTrabajos[i].fechaEntrada = moment(moment(dataTrabajos[i].fechaEntrada, 'YYYY-MM-DD')).format('DD-MM-YYYY');
            if (dataTrabajos[i].fechaSalida) {
                dataTrabajos[i].fechaSalida = moment(moment(dataTrabajos[i].fechaSalida, 'YYYY-MM-DD')).format('DD-MM-YYYY');
            } else {
                dataTrabajos[i].fechaSalida = 'PENDIENTE';
            }
        }
        //Ordenamos alfabeticamente el array por clientes
        dataTrabajos.sort((a, b) => {
            let fa = a.cliente.razonSocial;
            fb = b.cliente.razonSocial;
            if (fa < fb) {
                return -1;
            }
            if (fa > fb) {
                return 1;
            }
            return 0;
        });
        //Filtramos para que aparezca una sola vez el nombre
        clientes = [];
        for (var i = 0; i < dataTrabajos.length; i++) {
            if (clientes.find(cliente => cliente === dataTrabajos[i].cliente.razonSocial)) {
                dataTrabajos[i].cliente.razonSocial = '';
            } else {
                clientes.push(dataTrabajos[i].cliente.razonSocial);
            }
        }
        //Asignamos las variables a la estructura
        reporte.items.cliente = $('select[name="selectCliente"]').val();
        reporte.items.modelo = $('select[name="selectModelo"]').val();
        reporte.items.usuarioAsignado = $('select[name="selectUsuario"]').val();
        reporte.items.fechaDesde = fechaInicio;
        reporte.items.fechaHasta = fechaFin;
        reporte.items.excluirEntregados = checkEntregados;
        reporte.items.excluirCancelados = checkCancelados;
        reporte.items.verPendientes = checkPendientes;
        reporte.items.verPlanificados = checkPlanificados;
        reporte.items.verEnProceso = checkEnProceso;
        reporte.items.verFinalizados = checkFinalizados;
        reporte.items.trabajos = dataTrabajos;
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
    document.getElementById("filters1").style.display = "none";
    document.getElementById("filters2").style.display = "none";
    document.getElementById("filters3").style.display = "none";
    //Inicializamos SELECT2
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    //Excluir los generales
    document.getElementById("excluirEntregados").checked = false;
    document.getElementById("excluirCancelados").checked = true;
    //Ver los Particulares
    document.getElementById("verPendientes").checked = false;
    document.getElementById("verPlanificados").checked = false;
    document.getElementById("verEnProceso").checked = false;
    document.getElementById("verFinalizados").checked = false;
    //Inicializamos el Filtro de Rango de Fechas
    $('input[name="filterRangoFechas"]').daterangepicker({
        // autoUpdateInput: false,
        locale: {
            placeholder: 'Seleccione Rango de Fechas',
            format: 'DD-MM-YYYY',
            language: 'es',
            cancelLabel: 'Cancelar',
            applyLabel: 'Aplicar',
            theme: 'bootstrap4',
        },
        //Remover Botones de Aplicar y Cancelar
        autoApply: true,
    });
    //Extendemos el Datatables para asignar el formato de fecha
    $.fn.dataTable.moment('DD-MM-YYYY');
    //Inicializamos limpio el Filtro de Rango de Fechas
    $('input[name="filterRangoFechas"]').val('');
});