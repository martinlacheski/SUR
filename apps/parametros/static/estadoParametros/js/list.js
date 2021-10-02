$(function () {
    $('#data').DataTable({
        paging: false,
        searching: false,
        ordering: false,
        responsive: true,
        autoWidth: false,
        info: false,
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
            {"data": "estadoInicial.nombre"},
            {"data": "estadoEspecial.nombre"},
            {"data": "estadoFinalizado.nombre"},
            {"data": "estadoEntregado.nombre"},
            {"data": "estadoCancelado.nombre"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-6],
                class: 'text-center',
                render: function (data, type, row) {
                    if ( row.estadoInicial !== null) {
                        return row.estadoInicial.nombre
                    } else {
                        return ''
                    }
                }
            },
            {
                targets: [-5],
                class: 'text-center',
                render: function (data, type, row) {
                    if ( row.estadoEspecial !== null) {
                        return row.estadoEspecial.nombre
                    } else {
                        return ''
                    }
                }
            },
            {
                targets: [-4],
                class: 'text-center',
                render: function (data, type, row) {
                    if ( row.estadoFinalizado !== null) {
                        return row.estadoFinalizado.nombre
                    } else {
                        return ''
                    }
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                render: function (data, type, row) {
                    if ( row.estadoEntregado !== null) {
                        return row.estadoEntregado.nombre
                    } else {
                        return ''
                    }
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    if ( row.estadoCancelado !== null) {
                        return row.estadoCancelado.nombre
                    } else {
                        return 'SIN ESTADO'
                    }
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/estados-trabajo-parametros/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});