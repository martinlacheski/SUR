$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            //{"data": "id"},
            {"data": "nombre"},
            {"data": "nombre"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/paises/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/paises/update/' + row.id + '/" id="' + row.id +'" onclick="btnEliminar(this.id, this.href)" class="btn btn-danger btn-xs btn-flat" data-toggle="modal" data-target="#deleteModal"><i class="fas fa-trash-alt"></i>';

                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
    function btnEliminar() {
        console.log("entra al clic");
        // $('#deleteModal').modal('show');
        // console.log(row.id);
    }
});