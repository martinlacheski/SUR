var tablaProductos;
var tablaServicios;
var percepcionPorcentaje = 0.00;
//Definimos una estructura en JS para crear la venta
var venta = {
    items: {
        tipoComprobante: '',
        usuario: '',
        fecha: '',
        cliente: '',
        condicionVenta: '',
        medioPago: '',
        subtotal: 0.00,
        iva: 0.00,
        percepcion: 0.00,
        total: 0.00,
        //detalle de productos
        productos: [],
        //detalle de servicios
        servicios: []
    },

    //Funcion Agregar Producto al Array
    addProducto: function (item) {
        this.items.productos.push(item);
        this.listProductos();
    },
    //Funcion Agregar Servicio al Array
    addServicio: function (item) {
        this.items.servicios.push(item);
        this.listServicios();
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
            data: venta.items.productos,
            columns: [
                {"data": "id"}, //Para el boton eliminar
                {"data": "descripcion"},
                {"data": "precioVenta"},
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
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="Text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
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
    //----------------------------------------------------------------------------//
    //Listar los servicios en el Datatables
    listServicios: function () {
        calcular_importes();
        //this.calculate_invoice();
        tablaServicios = $('#tablaServicios').DataTable({
            paging: false,
            searching: false,
            ordering: false,
            //info: false,
            responsive: true,
            lengthMenu: [25, 50, 75, 100],
            autoWidth: false,
            destroy: true,
            data: this.items.servicios,
            columns: [
                {"data": "id"}, //Para el boton eliminar
                {"data": "descripcion"},
                {"data": "precioVenta"},
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
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="Text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
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
// agregar al campo numerico lo siguiente
//onkeypress="return isNumberKey(event)"
function isNumberKey(evt) {
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode < 48 || charCode > 57)
        return false;
    return true;
}
;

//Funcion para validar que el email tenga el formato correcto
function isValidEmail(mail) {
    return /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$/.test(mail);
};

//Funcion para Calcular los importes
function calcular_importes() {
    //Inicializamos variables para calcular importes
    var subtotal = 0.00;
    var ivaCalculado = 0.00;
    var percepcion = 0.00;
    //Recorremos el Array de productos para ir actualizando los importes
    $.each(venta.items.productos, function (pos, dict) {
        dict.pos = pos;
        dict.subtotal = dict.cantidad * parseFloat(dict.precioVenta);
        ivaCalculado += dict.subtotal * (dict.iva.iva / 100);
        subtotal += dict.subtotal;
    });
    //Recorremos el Array de servicios para ir actualizando los importes
    $.each(venta.items.servicios, function (pos, dict) {
        dict.pos = pos;
        dict.subtotal = dict.cantidad * parseFloat(dict.precioVenta);
        ivaCalculado += dict.subtotal * (dict.iva.iva / 100);
        subtotal += dict.subtotal;
    });
    //Asignamos los valores a los campos
    venta.items.subtotal = subtotal - ivaCalculado;
    venta.items.iva = ivaCalculado;
    venta.items.percepcion = percepcion;
    if (percepcionPorcentaje > 0) {
        venta.items.percepcion = venta.items.subtotal * (percepcionPorcentaje / 100);
        venta.items.total = venta.items.subtotal + venta.items.iva + venta.items.percepcion;
    } else {
        venta.items.percepcion = percepcion;
        venta.items.total = venta.items.subtotal + venta.items.iva;
    }
    $('input[name="subtotal"]').val(venta.items.subtotal.toFixed(2));
    $('input[name="iva"]').val(venta.items.iva.toFixed(2));
    $('input[name="percepcion"]').val(venta.items.percepcion.toFixed(2));
    $('input[name="total"]').val(venta.items.total.toFixed(2));
};

//Funcion para buscar la percepcion del cliente
function searchPercepcion() {
    var id = $('select[name="cliente"]').val();
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrftoken,
            'action': 'search_percepcion',
            'pk': id
        },
        dataType: 'json',
        success: function (data) {
            percepcionPorcentaje = parseFloat(data.percepcion);
        }
    });
};

//Inicializamos a CERO los campos de importes
$(document).ready(function () {
    var accion = $('input[name="action"]').val();
    if (accion === 'add') {
        $('input[name="subtotal"]').val('0.00');
        $('input[name="iva"]').val('0.00');
        $('input[name="percepcion"]').val('0.00');
        $('input[name="total"]').val('0.00');
        $('select[name="tipoComprobante"]').val(null).trigger('change');
        $('select[name="cliente"]').val(null).trigger('change');
        $('select[name="condicionVenta"]').val(null).trigger('change');
        $('select[name="medioPago"]').val(null).trigger('change');
        $('input[name="searchProductos"]').attr('disabled', true);
        $('input[name="searchServicios"]').attr('disabled', true);
        //Inicialización de datetimepicker
        $('#fecha').datetimepicker({
            format: 'DD-MM-YYYY',
            date: moment(),
            locale: 'es',
            maxDate: moment(),
        });
    } else {
        $('#fecha').datetimepicker({
            format: 'DD-MM-YYYY',
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
                console.log(data);
                //asignamos el detalle a la estructura
                venta.items.productos = data;
                //actualizamos el listado de productos
                venta.listProductos();
            }
        });
        //Buscamos el detalle de los servicios por ajax
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'get_detalle_servicios',
            },
            dataType: 'json',
            success: function (data) {
                console.log(data);
                //asignamos el detalle a la estructura
                venta.items.servicios = data;
                //actualizamos el listado de productos
                venta.listServicios();
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

    //Inicializamos el Datatable de Servicios
    $('#tablaServicios').DataTable({
        paging: false,
        searching: false,
        ordering: false,
        //info: false,
        responsive: true,
        lengthMenu: [25, 50, 75, 100],
        autoWidth: false,
    });


    //Inicializamos los campos de tipo TOUCHSPIN
    $("input[name='limiteCtaCte']").TouchSpin({
        min: 0,
        max: 1000000,
        step: 100,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '$'
    });

    $("input[name='plazoCtaCte']").TouchSpin({
        min: 0,
        max: 1000000,
        step: 1,
        boostat: 5,
        maxboostedstep: 10,
        postfix: 'Días'
    });

    //Verificamos que la fecha no sea mayor a la actual
    $('input[name="fecha"]').on('blur', function () {
        var fecha = $('input[name="fecha"]').val();
        var now = moment().format('DD-MM-YYYY');
        if (fecha > now) {
            error_action('Error', 'La fecha de venta no puede ser superior a la actual', function () {
                //pass
            }, function () {
                $('input[name="fecha"]').val(moment().format('DD-MM-YYYY'));
            });

        }
    });

//----------------------Buscamos si el cliente tiene Percepcion-----------------------------//
    $('select[name="cliente"]').on('change', function () {
        var id = $('select[name="cliente"]').val();
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'search_percepcion',
                'pk': id
            },
            dataType: 'json',
            success: function (data) {
                //asignamos a la variable global el porcentaje de percepcion
                percepcionPorcentaje = parseFloat(data.percepcion);
                //actualizamos los importes
                calcular_importes();
            }
        });
        if (id !== null && id !== '' && id !== undefined) {
            $('input[name="searchProductos"]').attr('disabled', false);
            $('input[name="searchServicios"]').attr('disabled', false);
        } else {
            $('input[name="searchProductos"]').attr('disabled', true);
            $('input[name="searchServicios"]').attr('disabled', true);
        }
    });

//------------------------------------MODAL CLIENTES----------------------------------------//
    //Boton Cliente Modal Mostrar
    $('.btnAddCliente').on('click', function () {
        $('#modalCliente').modal('show');
    });

    //Al cerrar el Modal de Cliente reseteamos los valores del formulario
    $('#modalCliente').on('hidden.bs.modal', function (e) {
        //Reseteamos los input del Modal
        $('#formCliente').trigger('reset');
        //Reseteamos los Select2 del Modal
        $(".condicionIvaFormCliente").val('').trigger('change.select2');
        $(".localidadFormCliente").val('').trigger('change.select2');
        $(".condicionPagoFormCliente").val('').trigger('change.select2');
        var errorList = document.getElementById("errorListFormCliente");
        errorList.innerHTML = '';
    });

    //CHECKBOX Cta Cte
    $('#ctaCte').on('click', function () {
        if (this.checked) {
            $('input[name="limiteCtaCte"]').attr('disabled', false);
            $('input[name="plazoCtaCte"]').attr('disabled', false);
            $('input[name="limiteCtaCte"]').attr('readonly', false);
            $('input[name="plazoCtaCte"]').attr('readonly', false);
            $('input[name="plazoCtaCte"]').trigger("touchspin.updatesettings", {min: 0});
            $('input[name="plazoCtaCte"]').trigger("touchspin.updatesettings", {max: 1000000});
        } else {
            $('input[name="limiteCtaCte"]').val('0.00');
            $('input[name="plazoCtaCte"]').val(0);
            $('input[name="limiteCtaCte"]').attr('readonly', true);
            $('input[name="plazoCtaCte"]').attr('readonly', true);
            $('input[name="plazoCtaCte"]').trigger("touchspin.updatesettings", {min: 0});
            $('input[name="plazoCtaCte"]').trigger("touchspin.updatesettings", {max: 0});
        }
    });

    //Validamos EMAIL CORRECTO en el formulario de CLiente
    $("#email").on('focusout', function (e) {
        var btn = document.getElementById('btnAddCliente');
        var check = isValidEmail($('input[name="email"]').val());
        if (check == false) {
            //alert('Dirección de correo electrónico no válido');
            $("#errorEmail").removeAttr("hidden");
            btn.disabled = true;
            $("#email").focus();
        } else {
            $('#errorEmail').attr("hidden", "");
            btn.disabled = false;
        }
    });

    // VALIDAMOS LOS CAMPOS
    $("#razonSocial").validate();
    $("#condicionIVA").validate();
    $("#cuil").validate();
    $("#localidad").validate();
    $("#direccion").validate();
    $("#telefono").validate();
    $("#email").validate();

    //Funcion Mostrar Errores del Formulario Cliente
    function message_error_cliente(obj) {
        var errorList = document.getElementById("errorListFormCliente");
        errorList.innerHTML = '';
        if (typeof (obj) === 'object') {
            var li = document.createElement("h5");
            li.textContent = "Error:";
            errorList.appendChild(li);
            $.each(obj, function (key, value) {
                var li = document.createElement("li");
                li.innerText = value;
                errorList.appendChild(li);
            });
        }
    }

    //Creamos un nuevo Cliente desde el Modal
    $('#formCliente').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_cliente');
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
                var newOption = new Option(data.razonSocial, data.id, false, true);
                $('select[name="cliente"]').append(newOption).trigger('change');
                $('#modalCliente').modal('hide');
            } else {
                message_error_cliente(data.error);
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
                venta.addProducto(ui.item);
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
                    venta.addProducto(item);
                    $('input[name="searchProductos"]').val('');
                    $('input[name="searchProductos"]').focus();
                } else {
                    error_action('Error', 'No existe el producto con el código ingresado', function () {
                        //pass
                    }, function () {
                        $('input[name="searchProductos"]').val('');
                        $('input[name="searchProductos"]').focus();
                    });
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
                venta.items.productos.splice(tr.row, 1);
                //Actualizamos el Listado
                venta.listProductos();
            }, function () {
            });
        })
        //evento cambiar renglon (cantidad) del detalle
        .on('change', 'input[name="cantidad"]', function () {
            //asignamos a una variable la cantidad, en la posicion actual
            var cant = parseInt($(this).val());
            //Obtenemos la posicion del elemento a modificar dentro del Datatables
            var tr = tablaProductos.cell($(this).closest('td, li')).index();
            venta.items.productos[tr.row].cantidad = cant;
            //Actualizamos los importes
            calcular_importes();
            //Actualizamos el importe de subtotal en la Posicion correspondiente en cada modificación
            $('td:eq(4)', tablaProductos.row(tr.row).node()).html('$' + venta.items.productos[tr.row].subtotal.toFixed(2));
        });

//Borrar desde el boton de busqueda de productos
    $('.btnClearSearchProductos').on('click', function () {
        $('input[name="searchProductos"]').val('').focus();
    });
//Borrar todos los productos
    $('.btnRemoveAllProductos').on('click', function () {
        if (venta.items.productos.length === 0) return false;
        //Ejecutar la Funcion de Confirmacion
        confirm_action('Confirmación', '¿Estas seguro de eliminar todos los registros?', function () {
            //removemos el listado de productos
            venta.items.productos = [];
            //Actualizamos el Listado
            venta.listProductos();
        }, function () {
        });
    });

//------------------------------------EVENTOS SERVICIOS----------------------------------------//
// Buscar Servicios
    $('input[name="searchServicios"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_servicios',
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
            venta.addServicio(ui.item);
            $(this).val('');
        },
    }).on('keydown', function (evt) {
        if (evt.key === "Enter" || evt.keyCode === 13) {
            evt.preventDefault();
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'get_servicio',
                    'term': $(this).val()
                },
                dataType: 'json',
                headers: {
                    'X-CSRFToken': csrftoken
                },
            }).done(function (data) {
                if (!data.hasOwnProperty('error')) {
                    var item = (data.servicio);
                    item.cantidad = 1;
                    item.subtotal = 0.00;
                    venta.addServicio(item);
                    $('input[name="searchServicios"]').val('');
                    $('input[name="searchServicios"]').focus();
                } else {
                    error_action('Error', 'No existe el servicio con el código ingresado', function () {
                        //pass
                    }, function () {
                        $('input[name="searchServicios"]').val('');
                        $('input[name="searchServicios"]').focus();
                    });
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
            }).always(function (data) {
            });
        }
    });
    // eventos tabla Servicios
    $('#tablaServicios tbody')
        //Evento eliminar renglon del detalle
        .on('click', 'a[rel="remove"]', function () {
            //obtenemos la posicion del datatables
            var tr = tablaServicios.cell($(this).closest('td, li')).index();
            //Ejecutar la Funcion de Confirmacion
            confirm_action('Confirmación', '¿Estas seguro de eliminar el registro?', function () {
                //removemos la posicion del array con la cantidad de elementos a eliminar
                venta.items.servicios.splice(tr.row, 1);
                //Actualizamos el Listado
                venta.listServicios();
            }, function () {
            });
        })
        //evento cambiar renglon (cantidad) del detalle
        .on('change', 'input[name="cantidad"]', function () {
            //asignamos a una variable la cantidad, en la posicion actual
            var cant = parseInt($(this).val());
            //Obtenemos la posicion del elemento a modificar dentro del Datatables
            var tr = tablaServicios.cell($(this).closest('td, li')).index();
            venta.items.servicios[tr.row].cantidad = cant;
            //Actualizamos los importes
            calcular_importes();
            //Actualizamos el importe de subtotal en la Posicion correspondiente en cada modificación
            $('td:eq(4)', tablaServicios.row(tr.row).node()).html('$' + venta.items.servicios[tr.row].subtotal.toFixed(2));
        });

    //Borrar desde el boton de busqueda de productos
    $('.btnClearSearchServicios').on('click', function () {
        $('input[name="searchServicios"]').val('').focus();
    });

    //Borrar todos los Servicios
    $('.btnRemoveAllServicios').on('click', function () {
        if (venta.items.servicios.length === 0) return false;
        //Ejecutar la Funcion de Confirmacion
        confirm_action('Confirmación', '¿Estas seguro de eliminar todos los registros?', function () {
            //removemos el listado de servicios
            venta.items.servicios = [];
            //Actualizamos el Listado
            venta.listServicios();
        }, function () {
        });
    });

    // Submit VENTA
    $('#ventaForm').on('submit', function (e) {
        e.preventDefault();
        if (venta.items.productos.length === 0 && venta.items.servicios.length === 0) {
            error_action('Error', 'Debe al menos tener un producto o servicio en sus detalles', function () {
                //pass
            }, function () {
                //pass
            });
        } else {
            confirm_action('Confirmación', '¿Estas seguro de realizar la siguiente acción?', function () {
                //realizamos la venta mediante Ajax
                venta.items.tipoComprobante = $('select[name="tipoComprobante"]').val();
                venta.items.condicionVenta = $('select[name="condicionVenta"]').val();
                venta.items.medioPago = $('select[name="medioPago"]').val();
                venta.items.fecha = moment(moment($('input[name="fecha"]').val(), 'DD-MM-YYYY')).format('YYYY-MM-DD');
                console.log(venta.items.fecha);
                venta.items.cliente = $('select[name="cliente"]').val();
                var parameters = new FormData();
                //Pasamos la accion ADD
                parameters.append('action', $('input[name="action"]').val());
                //Agregamos la estructura de Venta con los detalles correspondientes
                parameters.append('venta', JSON.stringify(venta.items));
                //Bloque AJAX VENTA
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
                            /*alert_action('Notificación', '¿Desea imprimir la boleta de venta?', function () {
                            window.open('/erp/sale/invoice/pdf/' + response.id + '/', '_blank');
                            location.href = '/erp/sale/list/';
                            }, function () {
                            location.href = '/erp/sale/list/';
                            });*/
                            location.replace(data.redirect);
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
            });
        }
        ;
    });
});

