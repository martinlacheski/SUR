var estadoInicial = 0;
var estadoPlanificado = 0;
var estadoEspecial = 0;
var estadoFinalizado = 0;
var estadoEntregado = 0;
var estadoCancelado = 0;
var tablaTrabajos;
var tablaPlanificacion;
var ordenTrabajos = 0;
var fechaInicio = '';
var fechaFin = '';
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
        //Recorremos el ARRAY para asignar el orden como corresponde
        for (var i = 0; i < planificacion.items.trabajos.length; i++) {
            planificacion.items.trabajos[i].orden = i + 1;
        }
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
                {"data": "orden"},
                {"data": "id"},
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
                        var buttons = '<a rel="subir" class="btn btn-primary btn-xs btn-flat" style="color: white;" ><i class="fas fa-arrow-up"></i></a> ';
                        buttons += '<a rel="bajar" class="btn btn-secondary btn-xs btn-flat" style="color: white;" ><i class="fas fa-arrow-down"></i></a> ';
                        buttons += '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;" ><i class="fas fa-trash-alt"></i></a> ';
                        return buttons
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
    //Extendemos el Datatables para asignar el formato de fecha
    $.fn.dataTable.moment('DD-MM-YYYY');
    var accion = $('input[name="action"]').val();
    if (accion === 'add') {
        //Inicialización de datetimepicker
        $('input[name="rangoFechas"]').daterangepicker({
            // autoUpdateInput: false,
            locale: {
                placeholder: 'Seleccione Rango de Fechas',
                format: 'DD-MM-YYYY',
                language: 'es',
                cancelLabel: 'Cancelar',
                applyLabel: 'Aplicar',
                theme: 'bootstrap4',
                minDate: moment(),
            },
            //Remover Botones de Aplicar y Cancelar
            autoApply: true,
        });
    } else {
        //Buscamos la fecha de inicio y de fin
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'get_fechas_planificacion',
            },
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataType: 'json',
            success: function (data) {
                fechaInicio = data.inicio;
                fechaFin = data.fin;
                $('input[name="rangoFechas"]').val(data.inicio + ' - ' + data.fin).attr('disabled', true);
            }
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
})
;

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
            {"data": "fechaEntrada"},
            {"data": "estadoTrabajo.nombre"},
            {"data": "modelo.nombre"},
            {"data": "cliente.razonSocial"},
            {"data": "id"}, //va duplicado algun campo por la botonera
        ],
        columnDefs: [
            {
                targets: [0],
                class: 'text-center',
                render: function (data, type, row) {
                    return moment(moment(data, 'YYYY-MM-DD')).format('DD-MM-YYYY');
                }

            },
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
            var accion = $('input[name="action"]').val();
            if (accion === 'add') {
                //Agregamos el Trabajo al Array de Planificacion
                ordenTrabajos = ordenTrabajos + 1;
                trabajo.orden = ordenTrabajos;
            } else if (accion === 'edit') {
                //Creamos una variable temporal del ultimo objeto de array
                var ultimoTrabajo = planificacion.items.trabajos[planificacion.items.trabajos.length - 1];
                //Si el Array tiene algun trabajo asignamos al orden siguiente
                if (ultimoTrabajo !== null && ultimoTrabajo !== '' && ultimoTrabajo !== undefined) {
                    //Agregamos el Trabajo al Array de Planificacion
                    ordenTrabajos = ultimoTrabajo.orden + 1;
                    trabajo.orden = ordenTrabajos;
                    //Asignamos el valor en 1
                } else {
                    trabajo.orden = 1;
                }
            }
            planificacion.addTrabajo(trabajo);
            //Una vez cargado el trabajo, sacamos del listado del Datatables
            tablaTrabajos.row($(this).parents('tr')).remove().draw();
        });
    $('#dataPlanificacion tbody')
        //Evento subir trabajo de posicion
        .on('click', 'a[rel="subir"]', function () {
            //Asignamos a una variable el renglon que necesitamos
            var tr = tablaPlanificacion.cell($(this).closest('td, li')).index();
            var pos = tr.row;
            if (pos > 0) {
                //Asignamos a una variable el trabajo temporal a mover de posicion
                var trabajoTemp = planificacion.items.trabajos[tr.row - 1];
                //Cambiamos el orden del trabajo temporal
                trabajoTemp.orden = trabajoTemp.orden + 1;
                //Asignamos el nuevo orden al que subimos
                planificacion.items.trabajos[tr.row].orden = planificacion.items.trabajos[tr.row].orden - 1;
                //subimos de posicion el trabajo
                planificacion.items.trabajos.splice(tr.row - 1, 0, planificacion.items.trabajos[tr.row]);
                //Borramos el trabajo que movimos de posicion
                planificacion.items.trabajos.splice(tr.row + 1, 1);
                //Insertamos el trabajo temporal
                planificacion.items.trabajos.splice(tr.row, 0, trabajoTemp);
                //Una vez insertado, eliminamos el trabajo original
                planificacion.items.trabajos.splice(tr.row, 1);
                //Volvemos a listar los trabajos
                planificacion.listTrabajos();
            }
        })
        //Evento bajar trabajo de posicion
        .on('click', 'a[rel="bajar"]', function () {
            var lenght = planificacion.items.trabajos.length;
            //Asignamos a una variable el renglon que necesitamos
            var tr = tablaPlanificacion.cell($(this).closest('td, li')).index();
            var pos = tr.row;
            if (pos < lenght - 1) {
                //Asignamos a una variable el trabajo temporal a mover de posicion
                var trabajoTemp = planificacion.items.trabajos[tr.row + 1];
                //Cambiamos el orden del trabajo temporal
                trabajoTemp.orden = trabajoTemp.orden - 1;
                //Asignamos el nuevo orden al que subimos
                planificacion.items.trabajos[tr.row].orden = planificacion.items.trabajos[tr.row].orden + 1;
                //bajamos de posicion el trabajo
                planificacion.items.trabajos.splice(tr.row + 1, 0, planificacion.items.trabajos[tr.row]);
                //Borramos el trabajo que movimos de posicion
                planificacion.items.trabajos.splice(tr.row, 1);
                //Insertamos el trabajo temporal
                planificacion.items.trabajos.splice(tr.row, 0, trabajoTemp);
                //Una vez insertado, eliminamos el trabajo original
                planificacion.items.trabajos.splice(tr.row + 2, 1);
                //Volvemos a listar los trabajos
                planificacion.listTrabajos();
            }
        })
        //Evento quitar trabajo de la planificacion
        .on('click', 'a[rel="remove"]', function () {
            //Asignamos a una variable el renglon que necesitamos
            var tr = tablaPlanificacion.cell($(this).closest('td, li')).index();
            //Asignamos a una variable el trabajo en base al renglon
            var trabajo = tablaPlanificacion.row(tr.row).data();
            //removemos la posicion del array con la cantidad de elementos a eliminar
            planificacion.items.trabajos.splice(tr.row, 1);
            // console.log(tr.row);
            // for (var i = tr.row; i < planificacion.items.trabajos.length; i++) {
            //     planificacion.items.trabajos[i].orden = i + 1;
            // }
            planificacion.listTrabajos();
            //Una vez cargado el trabajo, sacamos del listado del Datatables
            tablaPlanificacion.row($(this).parents('tr')).remove().draw();
            //Incorporamos el trabajo a la tabla principal
            tablaTrabajos.row.add(trabajo).draw();
            //Ordenamos la tabla
            tablaTrabajos.order([0, 'asc']).draw();
            // Permitimos al Datatables que los elementos sean de tipo SORTABLE
        });

    //Aplicamos Filtro de Rango de FECHAS
    $('input[name="rangoFechas"]').on('apply.daterangepicker', function (ev, picker) {
        fechaInicio = picker.startDate.format('DD-MM-YYYY');
        fechaFin = picker.endDate.format('DD-MM-YYYY');
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
        if (planificacion.items.trabajos.length === 0) {
            error_action('Error', 'No hay trabajos planificados', function () {
                //pass
            }, function () {
                //pass
            });
        } else {
            var accion = $('input[name="action"]').val();
            if (accion === 'add') {
                //Buscamos si no hay otra planificacion en el rango de fechas ingresado
                $.ajax({
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'check_fechas_planificacion',
                        'inicio': moment(moment(fechaInicio, 'DD-MM-YYYY')).format('YYYY-MM-DD'),
                        'fin': moment(moment(fechaFin, 'DD-MM-YYYY')).format('YYYY-MM-DD'),
                    },
                    dataType: 'json',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                }).done(function (data) {
                    chequear = data.check;
                    console.log(chequear);
                    if (chequear == false) {
                        confirm_action('Confirmación', '¿Estas seguro de realizar la siguiente acción?', function () {
                                //realizamos la creacion de la PLanificacion mediante Ajax
                                planificacion.items.fechaInicio = moment(moment(fechaInicio, 'DD-MM-YYYY')).format('YYYY-MM-DD');
                                planificacion.items.fechaFin = moment(moment(fechaFin, 'DD-MM-YYYY')).format('YYYY-MM-DD');
                                var parameters = new FormData();
                                //Pasamos la Accion
                                parameters.append('action', $('input[name="action"]').val());
                                parameters.append('planificacion', JSON.stringify(planificacion.items));
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
            } else if (accion === 'edit') {
                confirm_action('Confirmación', '¿Estas seguro de realizar la siguiente acción?', function () {
                        //realizamos la creacion de la PLanificacion mediante Ajax
                        planificacion.items.fechaInicio = moment(moment(fechaInicio, 'DD-MM-YYYY')).format('YYYY-MM-DD');
                        planificacion.items.fechaFin = moment(moment(fechaFin, 'DD-MM-YYYY')).format('YYYY-MM-DD');
                        var parameters = new FormData();
                        //Pasamos la Accion
                        parameters.append('action', $('input[name="action"]').val());
                        parameters.append('planificacion', JSON.stringify(planificacion.items));
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
            }
        };
    });
});