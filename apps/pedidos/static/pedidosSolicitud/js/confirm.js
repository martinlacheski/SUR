var renglon;
var tablaProductos;
//Definimos una estructura en JS para crear la Solicitud de Pedido
var pedido = {
    items: {
        pedidoSolicitud: '',
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
                {"data": "producto.descripcion"},
                {"data": "proveedor.razonSocial"},
                {"data": "marcaOfertada"},
                {"data": "costo"},
                {"data": "cantidad"},
                {"data": "subtotal"},
                {"data": "id"}, //Para el boton Actualizar
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
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-3],
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
                        return '<a rel="update" class="btn btn-warning btn-xs btn-flat" style="color: black;" ><i class="fas fa-edit"></i></a>';
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
    },
};

//------------------------------------Funciones e Inicializaciones----------------------------------------//

//Funcion para Calcular los importes
function calcular_importes() {
    //Inicializamos variables para calcular importes
    var subtotal = 0.00;
    var ivaCalculado = 0.00;
    //Recorremos el Array de productos para ir actualizando los importes
    $.each(pedido.items.productos, function (pos, dict) {
        dict.pos = pos;
        dict.subtotal = dict.cantidad * parseFloat(dict.costo);
        ivaCalculado += dict.subtotal * (dict.producto.iva.iva / 100);
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
    $('input[name="id_pedido"]').val();
    var accion = $('input[name="action"]').val();
    if (accion === 'confirm') {
        //Buscamos el detalle de los productos por ajax
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'get_productos_pedidos',
            },
            dataType: 'json',
            success: function (data) {
                pedido.items.pedidoSolicitud = data[0].pedidoSolicitud.id
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
        //Evento Editar Precio del Producto del detalle
        .on('click', 'a[rel="update"]', function () {
            //Asignamos a una variable el renglon que necesitamos
            var tr = tablaProductos.cell($(this).closest('td, li')).index();
            renglon = tr.row;
            //Asignamos a una variable el producto en base al renglon
            var prod = pedido.items.productos[renglon];
            //Cargamos los valores del Producto en el modal
            $('input[name="idProductoUpdate"]').val(prod.producto.id);   //INPUT HIDDEN ID PRODUCTO
            $('input[name="actualizarProducto"]').val(prod.producto.descripcion);
            //Buscamos por AJAX el PROVEEDOR QUE REALIZO LA OFERTA Y LOS DEMAS
            //Buscamos el detalle de proveedores del pedido
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrftoken,
                    'action': 'get_detalle_proveedor',
                    'pk': prod.proveedor.id,
                    'pedidoSolicitud': pedido.items.pedidoSolicitud
                },
                dataType: 'json',
                success: function (data) {
                    // Colocamos en el select el usuario mas desocupado
                    $('select[name="actualizarProveedor"]').html('').select2({
                        theme: "bootstrap4",
                        language: 'es',
                        data: data
                    });
                }
            });
            $('input[name="actualizarMarcaOfertada"]').val(prod.marcaOfertada);
            $('input[name="actualizarPrecioCosto"]').val(parseFloat(prod.costoProducto).toFixed(2));
            $('#modalDetalleProducto').modal('show');
        });

    //----------------------Al seleccionar un Proveedor-----------------------------//

    $('select[name="actualizarProveedor"]').on('change', function () {
        var id = $('select[name="actualizarProveedor"]').val();
        var prod = $('input[name="idProductoUpdate"]').val();
        //Buscamos el detalle de de la cotizacion del proveedor seleccionado
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'get_detalle_cotizacion',
                'pk': id,
                'producto': prod,
            },
            dataType: 'json',
            success: function (data) {
                // Colocamos en el select el proveedor seleccionado y los demas
                $('select[name="actualizarProveedor"]').html('').select2({
                    theme: "bootstrap4",
                    language: 'es',
                    data: data[0].proveedores
                });
                // actualizamos los campos con los valores correspondientes
                $('input[name="actualizarMarcaOfertada"]').val(data[0].marcaOfertada);
                $('input[name="actualizarPrecioCosto"]').val(data[0].costo);
            }
        });
    });

    // Submit Actualizacion Detalle
    $('#formDetalleProducto').on('submit', function (e) {
        e.preventDefault();
        // actualizamos los campos con los valores correspondientes
        var proveedor = $('select[name="actualizarProveedor"]').val();
        var marcaOfertada = $('input[name="actualizarMarcaOfertada"]').val();
        var costoProducto = $('input[name="actualizarPrecioCosto"]').val();
        //Asignamos a una variable el renglon del pedido a modificar
        var renglonActualizar = pedido.items.productos[renglon];
        //Buscamos el proveedor con el ID
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'get_proveedor',
                'pk': proveedor,
            },
            dataType: 'json',
            success: function (data) {
                console.log(data[0].detallePedido);
                renglonActualizar.proveedor = data[0].proveedor;
                renglonActualizar.marcaOfertada = marcaOfertada;
                renglonActualizar.costo = costoProducto;
                renglonActualizar.pedidoDetalle = data[0].detallePedido.id;
                pedido.listProductos();
            }
        });

        $('#modalDetalleProducto').modal('hide');

        // var id = $('select[name="actualizarProveedor"]').val();
        // var prod = $('input[name="idProductoUpdate"]').val();
        // //Bloque AJAX Actualizacion de Pedido
        // $.ajax({
        //     url: window.location.pathname,
        //     type: 'POST',
        //     data: {
        //         'action': 'actualizar_detalle_pedido',
        //         'pk': id,
        //         'producto': prod,
        //     },
        //     dataType: 'json',
        //     headers: {
        //         'X-CSRFToken': csrftoken
        //     },
        // }).done(function (data) {
        //     if (!data.hasOwnProperty('error')) {
        //         // Actualizamos el Listado
        //         //Buscamos el detalle de los productos por ajax
        //         $.ajax({
        //             url: window.location.pathname,
        //             type: 'POST',
        //             data: {
        //                 'csrfmiddlewaretoken': csrftoken,
        //                 'action': 'get_productos_pedidos',
        //             },
        //             dataType: 'json',
        //             success: function (data) {
        //                 //asignamos el detalle a la estructura
        //                 pedido.items.productos = data;
        //                 //actualizamos el listado de productos
        //                 pedido.listProductos();
        //             }
        //         });
        //
        //
        //     }
        // }).fail(function (jqXHR, textStatus, errorThrown) {
        // }).always(function (data) {
        // });
        // $('#modalDetalleProducto').modal('hide');
    });
//------------------------------------SUBMIT CONFIRMAR PEDIDO----------------------------------------//

    // Submit PEDIDO
    $('#pedidoForm').on('submit', function (e) {
        var accion = $('input[name="action"]').val();
        console.log(accion);
        e.preventDefault();
        if (pedido.items.productos.length === 0) {
            error_action('Error', 'Debe al menos tener un producto en su detalle', function () {
                //pass
            }, function () {
                //pass
            });
        } else {
            confirm_action('Confirmación', '¿Estas seguro de realizar la siguiente acción?', function () {
                    //realizamos el pedido mediante Ajax
                    var parameters = new FormData();
                    //Pasamos la accion CONFIRM
                    parameters.append('action', $('input[name="action"]').val());
                    //Pasamos el ID de Pedido de Solicitud
                    pedido.items.pedidoSolicitud = $('input[name="id_pedido"]').val();
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
                            if (!data.hasOwnProperty('error')) {
                                confirm_action('Notificación', '¿Desea imprimir la nota de Pedido?', function () {
                                    window.open('/pedidos/realizados/pdf/' + data.id + '/', '_blank');
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