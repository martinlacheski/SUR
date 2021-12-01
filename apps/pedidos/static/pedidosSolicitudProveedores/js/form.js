var renglon;
var tablaProductos;
//Definimos una estructura en JS para crear la Solicitud de Pedido
var pedido = {
    items: {
        fecha: '',
        fechaLimite: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        //detalle de productos
        productos: [],
    },
    //Obtenemos los ID de los Productos en el listado para Excluir en las busquedas
    getProductosListado: function () {
        var ids = [];
        $.each(this.items.productos, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    //Funcion Agregar Producto al Array
    addProducto: function (item) {
        this.items.productos.push(item);
        this.listProductos();
    },
    //----------------------------------------------------------------------------//
    //Listar los productos en el Datatables
    listProductos: function () {
        calcular_importes();
        tablaProductos = $('#tablaProductos').DataTable({
            paging: false,
            searching: false,
            ordering: false,
            //info: false,
            responsive: true,
            lengthMenu: [25, 50, 75, 100],
            autoWidth: false,
            destroy: true,
            data: pedido.items.productos,
            columns: [
                {"data": "id"}, //Para el boton eliminar
                {"data": "descripcion"},
                {"data": "costo"},
                {"data": "cantidad"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;" ><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="Text" name="costo" class="form-control form-control-sm input-sm text-center" autocomplete="off" value="' + row.costo + '">';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="Text" name="cantidad" class="form-control form-control-sm input-sm text-center" autocomplete="off" value="' + row.cantidad + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-right',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            //Este metodo permite personalizar datos de la fila y celda, tanto al agregar como al eliminar
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                //a todos los componentes requeridos le agregamos la libreria Touchspin
                $(row).find('input[name="costo"]').TouchSpin({
                    min: 1,
                    max: 1000000,
                    step: 0.1,
                    decimals: 2,
                    boostat: 5,
                    maxboostedstep: 10,
                    prefix: '$'
                });
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: 1000000,
                    step: 1,
                    boostat: 5,
                    maxboostedstep: 10,
                });
            },
            initComplete: function (settings, json) {

            }
        });
    },
};

//------------------------------------Funciones e Inicializaciones----------------------------------------//

//Permitir solo numeros
//Agregar al campo numerico lo siguiente
//onkeypress="return isNumberKey(event)"
function isNumberKey(evt) {
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode < 48 || charCode > 57)
        return false;
    return true;
};

//Funcion para Calcular los importes
function calcular_importes() {
    //Inicializamos variables para calcular importes
    var subtotal = 0.00;
    var ivaCalculado = 0.00;
    //Recorremos el Array de productos para ir actualizando los importes
    $.each(pedido.items.productos, function (pos, dict) {
        dict.pos = pos;
        dict.subtotal = dict.cantidad * parseFloat(dict.costo);
        ivaCalculado += dict.subtotal * (dict.iva.iva / 100);
        subtotal += dict.subtotal;
    });
    //Asignamos los valores a los campos
    pedido.items.subtotal = subtotal;
    pedido.items.iva = ivaCalculado;
    pedido.items.total = pedido.items.subtotal + pedido.items.iva;
    $('input[name="subtotal"]').val(pedido.items.subtotal.toFixed(2));
    $('input[name="iva"]').val(pedido.items.iva.toFixed(2));
    $('input[name="total"]').val(pedido.items.total.toFixed(2));
};

//Inicializamos a CERO los campos de importes
$(document).ready(function () {
    var accion = $('input[name="action"]').val();
    if (accion === 'add') {
        $('input[name="subtotal"]').val('0.00');
        $('input[name="iva"]').val('0.00');
        $('input[name="total"]').val('0.00');
        //Buscamos si la solicitud es válida todavia
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'search_validez',
            },
            dataType: 'json',
            success: function (data) {
                console.log(data.ok);
                if (data.ok === 'si') {
                    console.log('solicitud válida');
                } else if (data.ok === 'no') {
                    location.replace(data.redirect);
                }
            }
        });
        //Buscamos el Listado de los productos que deben reponerse por ajax
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'search_cabecera',
            },
            dataType: 'json',
            success: function (data) {
                $('input[name="pedidoSolicitud"]').val(data.pedido);
                $('input[name="proveedor"]').val(data.proveedor);
                $('input[name="validoHasta"]').val(moment(data.validoHasta, 'YYYY-MM-DD HH:mm').format('DD-MM-YYYY HH:mm'));
            }
        });
        //Buscamos el Listado de los productos que deben reponerse por ajax
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'get_productos_pedidos',
            },
            dataType: 'json',
            success: function (data) {
                //asignamos el detalle a la estructura
                pedido.items.productos = data;
                //actualizamos el listado de productos
                pedido.listProductos();
            }
        });
    }
});

$(function () {
    //Llamamos a la funcion de Token
    getToken(name);

    //Inicializamos SELECT2
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    //Inicializamos el Datatable de Productos
    $('#tablaProductos').DataTable({
        paging: false,
        searching: false,
        ordering: false,
        //info: false,
        responsive: true,
        lengthMenu: [25, 50, 75, 100],
        autoWidth: false,
    });

//------------------------------------EVENTOS PRODUCTOS----------------------------------------//

    // eventos tabla Productos
    $('#tablaProductos tbody')
        //Evento eliminar renglon del detalle
        .on('click', 'a[rel="remove"]', function () {
            //obtenemos la posicion del datatables
            var tr = tablaProductos.cell($(this).closest('td, li')).index();
            //Ejecutar la Funcion de Confirmacion
            confirm_action('Confirmación', '¿Estas seguro de eliminar el registro?', function () {
                //removemos la posicion del array con la cantidad de elementos a eliminar
                pedido.items.productos.splice(tr.row, 1);
                //Actualizamos el Listado
                pedido.listProductos();
            }, function () {
            });
        })
        //evento cambiar renglon (cantidad) del detalle
        .on('change', 'input[name="cantidad"]', function () {
            //asignamos a una variable la cantidad, en la posicion actual
            var cant = parseInt($(this).val());
            //Obtenemos la posicion del elemento a modificar dentro del Datatables
            var tr = tablaProductos.cell($(this).closest('td, li')).index();
            pedido.items.productos[tr.row].cantidad = cant;
            //Actualizamos los importes
            calcular_importes();
            //Actualizamos el importe de subtotal en la Posicion correspondiente en cada modificación
            $('td:eq(4)', tablaProductos.row(tr.row).node()).html('$' + pedido.items.productos[tr.row].subtotal.toFixed(2));
        })
        //Evento Editar Precio del Producto del detalle
        .on('change', 'input[name="costo"]', function () {
            //asignamos a una variable la cantidad, en la posicion actual
            var costo = parseFloat($(this).val());
            //Obtenemos la posicion del elemento a modificar dentro del Datatables
            var tr = tablaProductos.cell($(this).closest('td, li')).index();
            pedido.items.productos[tr.row].costo = costo;
            //Actualizamos los importes
            calcular_importes();
            //Actualizamos el importe de subtotal en la Posicion correspondiente en cada modificación
            $('td:eq(4)', tablaProductos.row(tr.row).node()).html('$' + pedido.items.productos[tr.row].subtotal.toFixed(2));
        });

    //Resetear formulario
    $('.btnResetForm').on('click', function () {
        confirm_action('Confirmación', '¿Estas seguro de realizar la siguiente acción?', function () {
            //Buscamos el Listado de los productos que deben reponerse por ajax
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrftoken,
                    'action': 'resetear_formulario',
                    'pk': $('input[name="pedidoSolicitud"]').val(),
                },
                dataType: 'json',
                success: function (data) {
                    //asignamos el detalle a la estructura
                    pedido.items.productos = data;
                    //actualizamos el listado de productos
                    pedido.listProductos();
                }
            });
        }, function () {
            //pass
        });
    });

//------------------------------------SUBMIT PEDIDO----------------------------------------//
// Submit PEDIDO
    $('#pedidoForm').on('submit', function (e) {
        e.preventDefault();
        if (pedido.items.productos.length === 0) {
            error_action('Error', 'Debe al menos tener un producto en sus detalle', function () {
                //pass
            }, function () {
                //pass
            });
        } else {
            confirm_action('Confirmación', '¿Estas seguro de realizar la siguiente acción?', function () {
                    //realizamos el pedido mediante Ajax
                    pedido.items.fecha = moment(moment($('input[name="fecha"]').val(), 'DD-MM-YYYY')).format('YYYY-MM-DD');
                    pedido.items.fechaLimite = moment(moment($('input[name="fechaLimite"]').val(), 'DD-MM-YYYY HH:mm')).format('YYYY-MM-DD HH:mm');
                    var parameters = new FormData();
                    //Pasamos la accion ADD
                    parameters.append('action', $('input[name="action"]').val());
                    //Agregamos la estructura de PEDIDO con los detalles correspondientes
                    parameters.append('pedido', JSON.stringify(pedido.items));
                    //Bloque AJAX PEDIDO
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
                            if (data.ok === 'no') {
                                location.replace(data.redirect);
                            } else {
                                if (!data.hasOwnProperty('error')) {
                                    confirm_action('Notificación', '¿Desea imprimir la cotización enviada?', function () {
                                        window.open('/pedidos/solicitudes/pdf/' + data.id + '/', '_blank');
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
                        }
                    });
                }
                ,
                function () {
                    //pass
                }
            );
        }
        ;
    });
});