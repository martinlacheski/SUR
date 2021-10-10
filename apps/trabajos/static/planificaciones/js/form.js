var estadoInicial = 0;
var estadoPlanificado = 0;
var estadoEspecial = 0;
var estadoFinalizado = 0;
var estadoEntregado = 0;
var estadoCancelado = 0;
var tablaTrabajos;
var tablaPlanificacion;
var ordenTrabajos = 0;
var planificacion = {
    items: {
        fechaInicio: '',
        fechaFin: '',
        //detalle de trabajos
        trabajos: [],
    },
    //Funcion Agregar Trabajo al Array
    addTrabajo: function (item) {
        this.items.trabajos.push(item);
        this.listTrabajos();
    },
    //Listar los productos en el Datatables
    listTrabajos: function () {
        tablaPlanificacion = $('#dataPlanificacion').DataTable({
            responsive: true,
            autoWidth: false,
            info: false,
            ordering: false,
            searching: false,
            destroy: true,
            deferRender: true,
            paging: false,
            rowReorder: true,
            data: planificacion.items.trabajos,
            columns: [
                {"data": "id"},
                {"data": "orden"},
                {"data": "modelo.nombre"},
                {"data": "cliente.razonSocial"},
                {"data": "id"}, //Para el boton eliminar
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;" ><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-5, -4, -3, -2],
                    class: 'text-center',
                    orderable: false,
                },
            ],
            initComplete: function (settings, json) {

            }
        });
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

$(document).ready(function () {
    var accion = $('input[name="action"]').val();
    if (accion === 'add') {
        //Inicialización de datetimepicker
        $('#fechaInicio').datetimepicker({
            format: 'DD-MM-YYYY',
            date: moment(),
            locale: 'es',
            minDate: moment(),
        });
        //Inicialización de datetimepicker
        $('#fechaFin').datetimepicker({
            format: 'DD-MM-YYYY',
            date: moment(),
            locale: 'es',
            minDate: moment(),
        });
    } else {
        //Inicialización de datetimepicker
        $('#fechaInicio').datetimepicker({
            format: 'DD-MM-YYYY',
            locale: 'es',
        });
        //Inicialización de datetimepicker
        $('#fechaFin').datetimepicker({
            format: 'DD-MM-YYYY',
            locale: 'es',
        });
        //Buscamos el detalle de trabajos de la planificacion por ajax
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'get_detalle_planificacion',
            },
            dataType: 'json',
            success: function (data) {
                //asignamos el detalle a la estructura
                planificacion.items.trabajos = data;
                //actualizamos el listado de productos
                planificacion.listTrabajos();
            }
        });
    }
});

$(function () {
    //Buscamos los parametros de estado
    searchParametros();
    tablaTrabajos = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        info: false,
        searching: false,
        paging: false,
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
            {"data": "modelo.nombre"},
            {"data": "cliente.razonSocial"},
            {"data": "id"}, //va duplicado algun campo por la botonera
        ],
        columnDefs: [
            {
                targets: [1],
                class: 'text-center',
                render: function (data, type, row) {
                    if (row.estadoTrabajo.id == estadoInicial) {
                        return '<span class="badge badge-warning">' + row.estadoTrabajo.nombre + '</span>'
                    } else if (row.estadoTrabajo.id == estadoPlanificado) {
                        return '<span class="badge badge-danger">' + row.estadoTrabajo.nombre + '</span>'
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
                targets: [-5, -4, -3, -2],
                class: 'text-center',
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="addTrabajo" class="btn btn-success btn-xs btn-flat"><i class="fas fa-plus"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
    $('#data tbody')
        //Evento agregar trabajo a la planificacion
        .on('click', 'a[rel="addTrabajo"]', function () {
            //Asignamos a una variable el renglon que necesitamos
            var tr = tablaTrabajos.cell($(this).closest('td, li')).index();
            //Asignamos a una variable el trabajo en base al renglon
            var trabajo = tablaTrabajos.row(tr.row).data();
            //Agregamos el Trabajo al Array de Planificacion
            ordenTrabajos = ordenTrabajos + 1;
            trabajo.orden = ordenTrabajos;
            planificacion.addTrabajo(trabajo);
            //Una vez cargado el trabajo, sacamos del listado del Datatables
            tablaTrabajos.row($(this).parents('tr')).remove().draw();
        });
    $('#dataPlanificacion tbody')
        //Evento quitar trabajo de la planificacion
        .on('click', 'a[rel="remove"]', function () {
            //Asignamos a una variable el renglon que necesitamos
            var tr = tablaPlanificacion.cell($(this).closest('td, li')).index();
            //Asignamos a una variable el trabajo en base al renglon
            var trabajo = tablaPlanificacion.row(tr.row).data();
            //removemos la posicion del array con la cantidad de elementos a eliminar
            planificacion.items.trabajos.splice(tr.row, 1);
            //Una vez cargado el trabajo, sacamos del listado del Datatables
            tablaPlanificacion.row($(this).parents('tr')).remove().draw();
            //Incorporamos el trabajo a la tabla principal
            tablaTrabajos.row.add(trabajo).draw();
            //Ordenamos la tabla
            tablaTrabajos.order([0, 'asc']).draw();
            // Permitimos al Datatables que los elementos sean de tipo SORTABLE
        });

    $("#dataPlanificacion tbody").sortable({
        items: "tr",
        cursor: 'move',
        opacity: 0.6,
        update: function (event, ui) {
            var array = []
            $(this).children().each(function (index) {
                $(this).attr('data-position', (index + 1));
                planificacion.items.trabajos[index].orden = index + 1;
                // console.log($(this).attr('data-position'));
                // tablaPlanificacion.draw();
                array.push(planificacion.items.trabajos[index]);
            });
            console.log(array);
        }
    });

    //Chequeamos que la fecha de FIN sea mayor que la de INICIO
    $('input[name="fechaFin"]').on('blur', function () {
        var btn = document.getElementById('btnGuardar');
        btn.disabled = true;
        var inicio = $('input[name="fechaInicio"]').val();
        var fin = $('input[name="fechaFin"]').val();
        if (inicio >= fin) {
            error_action('Error', 'La fecha de fin debe ser mayor que la fecha de inicio', function () {
                //pass
            }, function () {
                //pass
            });
        } else {
            btn.disabled = false;
        }
    });

    //Funcion Mostrar Errores del Formulario
    function message_error(obj) {
        var errorList = document.getElementById("errorList");
        errorList.innerHTML = '';
        if (typeof (obj) === 'object') {
            var li = document.createElement("h5");
            li.textContent = "Error:";
            errorList.appendChild(li);
            $.each(obj, function (key, value) {
                var li = document.createElement("li");
                li.innerText = key + ': ' + value;
                errorList.appendChild(li);
            });
        } else {
            var li = document.createElement("h5");
            li.textContent = "Error:";
            errorList.appendChild(li);
            var li = document.createElement("li");
            li.innerText = obj;
            errorList.appendChild(li);
        }
    }

    //Llamamos a la funcion de Token
    getToken(name);
    var chequear = false;
    //Hacemos el envio del Formulario mediante AJAX
    $("#planificacionesForm").submit(function (e) {
        e.preventDefault();
        var inicio = moment(moment($('input[name="fechaInicio"]').val(), 'DD-MM-YYYY')).format('YYYY-MM-DD');
        var fin = moment(moment($('input[name="fechaFin"]').val(), 'DD-MM-YYYY')).format('YYYY-MM-DD');
        if (planificacion.items.trabajos.length === 0) {
            error_action('Error', 'No hay trabajos planificados', function () {
                //pass
            }, function () {
                //pass
            });
        } else if (inicio >= fin) {
            error_action('Error', 'La fecha de Fin debe ser mayor que la de inicio', function () {
                //pass
            }, function () {
                //pass
            });
        } else {
            //Buscamos si no hay otra planificacion en el rango de fechas ingresado

            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'check_fechas_planificacion',
                    'inicio': inicio,
                    'fin': fin,
                },
                dataType: 'json',
                headers: {
                    'X-CSRFToken': csrftoken
                },
            }).done(function (data) {
                chequear = data.check;
                if (chequear == true) {
                    confirm_action('Confirmación', '¿Estas seguro de realizar la siguiente acción?', function () {
                            //realizamos la creacion de la PLanificacion mediante Ajax
                            planificacion.items.fechaInicio = moment(moment($('input[name="fechaInicio"]').val(), 'DD-MM-YYYY')).format('YYYY-MM-DD');
                            planificacion.items.fechaFin = moment(moment($('input[name="fechaFin"]').val(), 'DD-MM-YYYY')).format('YYYY-MM-DD');
                            var parameters = new FormData();
                            //Pasamos la Accion
                            parameters.append('action', $('input[name="action"]').val());
                            parameters.append('planificacion', JSON.stringify(planificacion.items));
                            // if (ordenTrabajos !== undefined) {
                            //     parameters.append('trabajos', JSON.stringify(ordenTrabajos));
                            //     parameters.append('trabajos', JSON.stringify(ordenTrabajos));
                            // } else {
                            //
                            // }
                            //Bloque AJAX PLANIFICACION
                            $.ajax({
                                url: window.location.href,
                                type: 'POST',
                                data: parameters,
                                dataType: 'json',
                                headers: {
                                    'X-CSRFToken': csrftoken
                                },
                                processData: false,
                                contentType: false,
                                success: function (data) {
                                    if (!data.hasOwnProperty('error')) {
                                        confirm_action('Notificación', '¿Desea imprimir la planificacion?', function () {
                                            window.open('/planificaciones/pdf/' + data.id + '/', '_blank');
                                            location.replace(data.redirect);
                                        }, function () {
                                            location.replace(data.redirect);
                                        });
                                        //location.replace(data.redirect);
                                    } else {
                                        error_action('Error', data.error, function () {
                                            //pass
                                        }, function () {
                                            //pass
                                        });
                                    }
                                }
                            });
                        }, function () {
                            //pass
                        }
                    );
                } else {
                    error_action('Error', 'Ya existe una planificación en ese rango de fechas', function () {
                        //pass
                    }, function () {
                        //pass
                    });
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
            }).always(function (data) {

            });
        }
    });
});