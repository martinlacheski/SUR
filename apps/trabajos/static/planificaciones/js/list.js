var tablaTrabajos;
var estadoInicial = 0;
var estadoPlanificado = 0;
var estadoEspecial = 0;
var estadoFinalizado = 0;
var estadoEntregado = 0;
var estadoCancelado = 0;
var countTrabajos = 0;

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
    //Eventos del Listado
    var tablaPlanificacion = $('#data').DataTable({
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
            {"data": "fechaInicio"},
            {"data": "fechaFin"},
            {"data": "cantidad"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [0],
                class: 'text-center',
            },
            {
                targets: [-4, -3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return moment(moment(data, 'YYYY-MM-DD')).format('DD-MM-YYYY');
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<span class="badge badge-success">' + row.cantidad + '</span>'
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="detallePlanificacion" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i></a> ';
                    buttons += '<a href="/planificaciones/pdf/' + row.id + '/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    buttons += '<a href="/planificaciones/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/planificaciones/delete/' + row.id + '/" id="' + row.id + '" onclick="btnEliminar(this.id, this.href)" class="btn btn-danger btn-xs btn-flat" data-toggle="modal" data-target="#deleteModal"><i class="fas fa-times"></i>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

    $('#data tbody')
        .on('click', 'a[rel="detallePlanificacion"]', function () {
            //Buscamos los parametros de estado
            searchParametros();
            //Seleccionamos el Presupuesto sobre la cual queremos traer el detalle
            var tr = tablaPlanificacion.cell($(this).closest('td, li')).index();
            var data = tablaPlanificacion.row(tr.row).data();

            //Cargamos el detalle de productos
            $('#tablaTrabajos').DataTable({
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
                        'action': 'search_detalle_trabajos',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "orden"},
                    {"data": "trabajo.id"},
                    {"data": "trabajo.modelo.nombre"},
                    {"data": "trabajo.cliente.razonSocial"},
                    {"data": "trabajo.estadoTrabajo"},
                ],
                columnDefs: [
                    {
                        targets: [-5, -4, -3, -2],
                        class: 'text-center',
                    },

                    {
                        targets: [-1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            if (row.trabajo.estadoTrabajo.id == estadoInicial) {
                                return '<span class="badge badge-warning">' + row.trabajo.estadoTrabajo.nombre + '</span>'
                            } else if (row.trabajo.estadoTrabajo.id == estadoPlanificado) {
                                return '<span class="badge badge-dark">' + row.trabajo.estadoTrabajo.nombre + '</span>'
                            } else if (row.trabajo.estadoTrabajo.id == estadoEspecial) {
                                return '<span class="badge badge-info">' + row.trabajo.estadoTrabajo.nombre + '</span>'
                            } else if (row.trabajo.estadoTrabajo.id == estadoFinalizado) {
                                return '<span class="badge badge-success">' + row.trabajo.estadoTrabajo.nombre + '</span>'
                            } else if (row.trabajo.estadoTrabajo.id == estadoCancelado) {
                                return '<span class="badge badge-danger">' + row.trabajo.estadoTrabajo.nombre + '</span>'
                            } else if (row.trabajo.estadoTrabajo.id == estadoEntregado) {
                                return '<span class="badge badge-primary">' + row.trabajo.estadoTrabajo.nombre + '</span>'
                            } else {
                                return '<span class="badge badge-info">' + row.trabajo.estadoTrabajo.nombre + '</span>'
                            }
                        }
                    },
                ],
                initComplete: function (settings, json) {

                }
            });
            $('#modalDetalle').modal('show');
        });

});