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
                    render: function (data, type, row) {
                        return '<input type="Text" name="cantidad" class="form-control form-control-sm input-sm text-center" autocomplete="off" value="' + row.cantidad + '">';
                    }
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
            //Este metodo permite personalizar datos de la fila y celda, tanto al agregar como al eliminar
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                //a todos los componentes llamado Cantidad le agregamos la libreria Touchspin
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
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'search_precioProducto',
                'pk': dict.id
            },
            dataType: 'json',
            success: function (data) {
                dict.costo = parseFloat(data);
                //Actualizamos el precio del list
                pedido.items.productos[pos].costo = parseFloat(data);
            }
        });
        dict.pos = pos;
        dict.subtotal = dict.cantidad * parseFloat(dict.costo);
        ivaCalculado += dict.subtotal * (dict.iva.iva / 100);
        subtotal += dict.subtotal;
    });
    //Asignamos los valores a los campos
    pedido.items.subtotal = subtotal - ivaCalculado;
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
        //Inicialización de datetimepicker
        $('#fecha').datetimepicker({
            format: 'DD-MM-YYYY',
            date: moment(),
            locale: 'es',
            maxDate: moment(),
        });
        //Inicialización de datetimepicker
        $('#fechaLimite').datetimepicker({
            format: 'DD-MM-YYYY HH:mm',
            locale: 'es',
            minDate: moment(),
            icons: {time: 'far fa-clock'},
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
    } else {
        $('#fecha').datetimepicker({
            format: 'DD-MM-YYYY',
            locale: 'es',
        });
        $('#fechaLimite').datetimepicker({
            format: 'DD-MM-YYYY HH:mm',
            locale: 'es',
        });
        //Buscamos el detalle de los productos por ajax
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'get_detalle_productos',
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
    //Al hacer click en el AYUDA
    $('.verAyuda').on('click', function () {
        introJs().setOptions({
            showProgress: true,
            showBullets: false,
            nextLabel: 'Siguiente',
            prevLabel: 'Atrás',
            doneLabel: 'Finalizar',
        }).start()
    });

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

    //Verificamos que la fecha no sea mayor a la actual
    $('input[name="fecha"]').on('blur', function () {
        var fecha = $('input[name="fecha"]').val();
        var now = moment().format('DD-MM-YYYY');
        if (fecha > now) {
            error_action('Error', 'La fecha de pedido no puede ser superior a la actual', function () {
                //pass
            }, function () {
                $('input[name="fecha"]').val(moment().format('DD-MM-YYYY'));
            });
        }
    });
    //Verificamos que la fechaLimite no sea menor a la fecha de Solicitud de Pedido
    $('input[name="fechaLimite"]').on('blur', function () {
        var fecha = $('input[name="fecha"]').val();
        var fechaPedido = moment(moment(fecha, 'DD-MM-YYYY')).format('YYYY-MM-DD HH:mm');
        var fechaLimite = moment(moment($('input[name="fechaLimite"]').val(), 'DD-MM-YYYY HH:mm')).format('YYYY-MM-DD HH:mm');
        if (fechaPedido > fechaLimite) {
            error_action('Error', 'La fecha límite no puede ser inferior a la fecha de pedido', function () {
                //pass
            }, function () {
                $('input[name="fechaLimite"]').val(moment().format('DD-MM-YYYY HH:mm'));
            });
        }
    });

//------------------------------------MODAL Buscar PRODUCTOS----------------------------------------//

    //Boton Buscar Productos Mostrar Modal
    $('.btnSearchProductos').on('click', function () {
        tablaSearchProductos = $('#tablaSearchProductos').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrftoken,
                    'excluir': JSON.stringify(pedido.getProductosListado()),
                    'action': 'search_all_productos',
                },
                dataSrc: ""
            },
            columns: [
                {"data": "subcategoria.nombre"},
                {"data": "descripcion"},
                {"data": "stockReal"},
                {"data": "precioVenta"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-5, -4],
                    class: 'text-center',
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.stockReal > 0) {
                            return '<span class="badge badge-success">' + data + '</span>'
                        }
                        return '<span class="badge badge-danger">' + data + '</span>'
                    }
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
                        var buttons = '<a rel="addProducto" class="btn btn-success btn-xs btn-flat"><i class="fas fa-plus"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
        $('#modalSearchProductos').modal('show');
    });

    $('#tablaSearchProductos tbody')
        .on('click', 'a[rel="addProducto"]', function () {
            //Asignamos a una variable el renglon que necesitamos
            var tr = tablaSearchProductos.cell($(this).closest('td, li')).index();
            //Asignamos a una variable el producto en base al renglon
            var producto = tablaSearchProductos.row(tr.row).data();
            producto.cantidad = 1;
            producto.subtotal = 0.00;
            pedido.addProducto(producto);
            //Una vez cargado el producto, sacamos del listado del Datatables
            tablaSearchProductos.row($(this).parents('tr')).remove().draw();
        });

//------------------------------------MODAL PRODUCTOS----------------------------------------//

    //Boton Agregar Producto Mostrar Modal
    $('.btnAddProducto').on('click', function () {
        //Inicializamos el Codigo del Producto
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'generar_codigo_producto',
            },
            dataType: 'json',
            success: function (data) {
                $('input[name="codigo"]').val(data.codigo);
            }
        });
        $('#modalProducto').modal('show');
    });

    //Inicializamos los campos de tipo TOUCHSPIN
    $("input[name='stockReal']").TouchSpin({
        min: -1000000,
        max: 1000000,
        step: 1,
        boostat: 5,
        maxboostedstep: 10,
    });
    $("input[name='stockMinimo']").TouchSpin({
        min: 0,
        max: 1000000,
        step: 1,
        boostat: 5,
        maxboostedstep: 10,
    });
    $("input[name='reposicion']").TouchSpin({
        min: 0,
        max: 1000000,
        step: 1,
        boostat: 5,
        maxboostedstep: 10,
    });
    $("input[name='costo']").TouchSpin({
        min: 0,
        max: 1000000,
        step: 0.1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '$'
    });
    $("input[name='utilidad']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    });
    $("input[name='precioVenta']").TouchSpin({
        min: 0,
        max: 10000000,
        step: 0.1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '$'
    });

    //Select Anidado (Seleccionamos CATEGORIA y cargamos las SUBCATEGORIAS de dicha CATEGORIA
    var select_subcategorias = $('select[name="subcategoria"]');
    $('.selectCategoria').on('change', function () {
        var id = $(this).val();
        var options = '<option value="">---------</option>';
        if (id === '') {
            select_subcategorias.html(options);
            return false;
        }
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'search_subcategorias',
                'pk': id
            },
            dataType: 'json',
            success: function (data) {
                if (!data.hasOwnProperty('error')) {
                    //Volvemos a cargar los datos del Select2 solo que los datos (data) ingresados vienen por AJAX
                    select_subcategorias.html('').select2({
                        theme: "bootstrap4",
                        language: 'es',
                        data: data
                    });
                }
            }
        });
    });

    //Al cerrar el Modal de Productos reseteamos los valores del formulario
    $('#modalProducto').on('hidden.bs.modal', function (e) {
        //Reseteamos los input del Modal
        $('#formProducto').trigger('reset');
        //Reseteamos los Select2 del Modal
        $(".subcategoria").val('').trigger('change.select2');
        $(".categoria").val('').trigger('change.select2');
        $(".iva").val('').trigger('change.select2');
        var errorList = document.getElementById("errorListFormProducto");
        errorList.innerHTML = '';
    });

    //Metodo para calcular el precio en base a los tres posibles cambios (COSTO UTILIDAD e IVA)
    $('input[name="costo"]').on('change', function () {
        calcularPrecio();
    });
    $('input[name="utilidad"]').on('change', function () {
        calcularPrecio();
    });
    $('select[name="iva"]').on('change', function () {
        calcularPrecio();
    });
    $('input[name="precioVenta"]').on('change', function () {
        calcularUtilidad();
    });

    //Funcion para calcular el precio entre COSTO UTILIDAD e IVA
    function calcularPrecio() {
        var id = $('select[name="iva"]').val();
        var iva = 0;
        var costo = $('input[name="costo"]').val();
        var utilidad = $('input[name="utilidad"]').val();
        utilidad = (utilidad / 100) + 1;
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'search_iva',
                'pk': id
            },
            dataType: 'json',
            success: function (data) {
                iva = (data.iva);
                iva = (iva / 100) + 1;
                if (iva > 0) {
                    var precio = (costo * utilidad * iva);
                    $('input[name="precioVenta"]').val(precio.toFixed(2));
                }
            }
        });
        if (iva > 0) {
            var precio = (costo * utilidad * iva);
            $('input[name="precioVenta"]').val(precio);
        }
    }

    //Funcion para calcular el precio entre COSTO IVA y TOTAL
    function calcularUtilidad() {
        var id = $('select[name="iva"]').val();
        var iva = 0;
        var costo = $('input[name="costo"]').val();
        var total = $('input[name="precioVenta"]').val();
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'search_iva',
                'pk': id
            },
            dataType: 'json',
            success: function (data) {
                iva = (data.iva);
                iva = (iva / 100) + 1;
                if (iva > 0) {
                    var precio = (((total / iva) / costo) - 1) * 100;
                    $('input[name="utilidad"]').val(precio.toFixed(2));
                }
            }
        });
        if (iva > 0) {
            var precio = (((total / iva) / costo) - 1) * 100;
            $('input[name="utilidad"]').val(precio);
        }
    }

    //agregar al campo numerico lo siguiente
    //onkeypress="return isNumberKey(event)"
    function isNumberKey(evt) {
        var charCode = (evt.which) ? evt.which : evt.keyCode;
        if (charCode < 48 || charCode > 57)
            return false;
        return true;
    }

    //Funcion Mostrar Errores del Formulario Producto
    function message_error_producto(obj) {
        var errorList = document.getElementById("errorListFormProducto");
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

    //Creamos un nuevo Producto desde el Modal
    $('#formProducto').on('submit', function (e) {
        // VALIDACION DE LOS CAMPOS
        $("#subcategoria").validate();
        $("#descripcion").validate();
        //$("#stockReal").validate();
        $("#stockMinimo").validate();
        $("#reposicion").validate();
        $("#costo").validate();
        $("#utilidad").validate();
        $("#iva").validate();
        $("#precioVenta").validate();
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_producto');
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            processData: false,
            contentType: false,
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                $('#modalProducto').modal('hide');
            } else {
                message_error_producto(data.error);
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
        }).always(function (data) {
        });
    });

//------------------------------------EVENTOS PRODUCTOS----------------------------------------//

//Buscar Productos
    $('input[name="searchProductos"]')
        .autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_productos',
                        'excluir': JSON.stringify(pedido.getProductosListado()),
                        'term': request.term
                    },
                    dataType: 'json',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                }).done(function (data) {
                    response(data);
                }).fail(function (jqXHR, textStatus, errorThrown) {
                }).always(function (data) {
                });
            },
            delay: 500,
            minLength: 1,
            select: function (event, ui) {
                event.preventDefault();
                ui.item.cantidad = 1;
                ui.item.subtotal = 0.00;
                pedido.addProducto(ui.item);
                $(this).val('');
            },
        }).on('keydown', function (evt) {
        if (evt.key === "Enter" || evt.keyCode === 13) {
            evt.preventDefault();
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'get_producto',
                    'excluir': JSON.stringify(pedido.getProductosListado()),
                    'term': $(this).val()
                },
                dataType: 'json',
                headers: {
                    'X-CSRFToken': csrftoken
                },
            }).done(function (data) {
                if (!data.hasOwnProperty('error')) {
                    var item = (data.producto);
                    item.cantidad = 1;
                    item.subtotal = 0.00;
                    pedido.addProducto(item);
                    $('input[name="searchProductos"]').val('');
                    $('input[name="searchProductos"]').focus();
                } else {
                    if (data.error == "El Producto ya se encuentra en el listado") {
                        error_action('Error', 'El Producto ya se encuentra en el listado', function () {
                            $('input[name="searchProductos"]').val('');
                            $('input[name="searchProductos"]').focus();
                        }, function () {
                            $('input[name="searchProductos"]').val('');
                            $('input[name="searchProductos"]').focus();
                        });
                    } else {
                        // error_action('Error', 'No existe el producto con el código ingresado', function () {
                        confirm_action('Error', 'No existe el producto, ¿Desea registrarlo?', function () {
                            $('#modalProducto').modal('show');
                            $('input[name="searchProductos"]').val('');
                            $('input[name="searchProductos"]').focus();
                        }, function () {
                            $('input[name="searchProductos"]').val('');
                            $('input[name="searchProductos"]').focus();
                        });
                    }

                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
            }).always(function (data) {
            });
        }
    });

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
        .on('click', 'a[rel="update"]', function () {
            //Asignamos a una variable el renglon que necesitamos
            var tr = tablaProductos.cell($(this).closest('td, li')).index();
            renglon = tr.row;
            //Asignamos a una variable el producto en base al renglon
            var prod = tablaProductos.row(tr.row).data();
            //Cargamos los valores del Producto en el modal
            $('input[name="idProductoUpdate"]').val(prod.id);   //INPUT HIDDEN ID PRODUCTO
            $('input[name="actualizarSubcategoria"]').val(prod.subcategoria.nombre);
            $('input[name="actualizarDescripcion"]').val(prod.descripcion);
            $('input[name="actualizarCosto"]').val(prod.costo)
                .TouchSpin({
                    min: 0,
                    max: 1000000,
                    step: 0.1,
                    decimals: 2,
                    boostat: 5,
                    maxboostedstep: 10,
                    postfix: '$'
                });
            $('input[name="actualizarUtilidad"]').val(prod.utilidad)
                .TouchSpin({
                    min: 0,
                    max: 1000,
                    step: 0.1,
                    decimals: 2,
                    boostat: 5,
                    maxboostedstep: 10,
                    postfix: '%'
                });
            $('input[name="actualizarIva"]').val(prod.iva.iva);
            $('input[name="actualizarPrecioVenta"]').val(prod.precioVenta)
                .TouchSpin({
                    min: 0,
                    max: 1000000,
                    step: 0.1,
                    decimals: 2,
                    boostat: 5,
                    maxboostedstep: 10,
                    postfix: '$'
                });
            $('#modalPrecioProducto').modal('show');

            //EN MODAL ACTUALIZAR PRECIO PRODUCTO
            // Metodo para calcular el precio en base a los tres posibles cambios (COSTO UTILIDAD y Precio Venta)
            $('input[name="actualizarCosto"]').on('change', function () {
                calcularPrecioActualizacion();
            });
            $('input[name="actualizarUtilidad"]').on('change', function () {
                calcularPrecioActualizacion();
            });
            $('input[name="actualizarPrecioVenta"]').on('change', function () {
                calcularUtilidadActualizacion();
            });
        });

//------------------------------------MODAL ACTUALIZAR PRECIO PRODUCTOS----------------------------------------//

    //Funcion para calcular el precio entre COSTO UTILIDAD e IVA
    function calcularPrecioActualizacion() {
        var iva = $('input[name="actualizarIva"]').val();
        var costo = $('input[name="actualizarCosto"]').val();
        var utilidad = $('input[name="actualizarUtilidad"]').val();
        utilidad = (utilidad / 100) + 1;
        iva = (iva / 100) + 1;
        var precio = (costo * utilidad * iva);
        $('input[name="actualizarPrecioVenta"]').val(precio.toFixed(2));
    }

    //Funcion para calcular el precio entre COSTO IVA y TOTAL
    function calcularUtilidadActualizacion() {
        var iva = $('input[name="actualizarIva"]').val();
        var costo = $('input[name="actualizarCosto"]').val();
        var total = $('input[name="actualizarPrecioVenta"]').val();
        iva = (iva / 100) + 1;
        var precio = (((total / iva) / costo) - 1) * 100;
        $('input[name="actualizarUtilidad"]').val(precio.toFixed(2));
    }

    //Actualizamos el precio del PRODUCTO desde el Modal
    $('#formPrecioProducto').on('submit', function (e) {
        e.preventDefault();
        confirm_action('Confirmación', '¿Estas seguro de realizar la siguiente acción?', function () {
            var id = $('input[name="idProductoUpdate"]').val();
            var costo = $('input[name="actualizarCosto"]').val();
            var utilidad = $('input[name="actualizarUtilidad"]').val();
            var precioVenta = $('input[name="actualizarPrecioVenta"]').val();
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'update_precioProducto',
                    'pk': id,
                    'costo': costo,
                    'utilidad': utilidad,
                    'precioVenta': precioVenta
                },
                dataType: 'json',
                headers: {
                    'X-CSRFToken': csrftoken
                },
            }).done(function (data) {
                if (!data.hasOwnProperty('error')) {
                    //Actualizamos el Listado
                    calcular_importes();
                    pedido.listProductos();
                    $('#modalPrecioProducto').modal('hide');

                } else {
                    message_error_precio_producto(data.error);
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
            }).always(function (data) {
            });
            //Asignamos a una variable el producto en base al renglon
            var prod = pedido.items.productos[renglon];
            //actualizamos el costo y subtotal del producto en el array
            prod.costo = costo;
            prod.subtotal = costo * prod.cantidad;
            //Actualizamos el valor del renglon del Datatables
            tablaProductos.row(renglon).data(prod).draw();
        }, function () {
            //pass
        });
    });

    //Funcion Mostrar Errores del Formulario Producto
    function message_error_precio_producto(obj) {
        var errorList = document.getElementById("errorListformPrecioProducto");
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

//Borrar desde el boton de busqueda de productos
    $('.btnClearSearchProductos').on('click', function () {
        $('input[name="searchProductos"]').val('').focus();
    });
//Borrar todos los productos
    $('.btnRemoveAllProductos').on('click', function () {
        if (pedido.items.productos.length === 0) return false;
        //Ejecutar la Funcion de Confirmacion
        confirm_action('Confirmación', '¿Estas seguro de eliminar todos los registros?', function () {
            //removemos el listado de productos
            pedido.items.productos = [];
            //Actualizamos el Listado
            pedido.listProductos();
        }, function () {
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
                    pedido.items.fechaLimite = moment(moment($('input[name="fechaLimite"]').val(), 'DD-MM-YYYY HH:mm')).format('YYYY-MM-DD HH:mm:ss');
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
                            if (!data.hasOwnProperty('error')) {
                                confirm_action('Notificación', '¿Desea imprimir la nota de Pedido?', function () {
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