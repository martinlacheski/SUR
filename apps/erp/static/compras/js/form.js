var tablaProductos;
var percepcionPorcentaje = 0.00;
//Definimos una estructura en JS para crear la COMPRA
var compra = {
    items: {
        usuario: '',
        fecha: '',
        proveedor: '',
        medioPago: '',
        tipoComprobante: '',
        nroComprobante: '',
        subtotal: 0.00,
        iva: 0.00,
        percepcion: 0.00,
        total: 0.00,
        //detalle de productos
        productos: [],
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
            data: compra.items.productos,
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
                        // return '$' + parseFloat(data).toFixed(2);
                        return '<input type="Text" name="costo" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.costo + '">';
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
                $(row).find('input[name="costo"]').TouchSpin({
                    min: 1,
                    max: 1000000,
                    step: 0.1,
                    decimals: 2,
                    boostat: 5,
                    maxboostedstep: 10,
                });
            },
            initComplete: function (settings, json) {

            }
        });
    },
    //----------------------------------------------------------------------------//
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
    $.each(compra.items.productos, function (pos, dict) {
        dict.pos = pos;
        dict.subtotal = dict.cantidad * parseFloat(dict.costo);
        ivaCalculado += dict.subtotal * (dict.iva.iva / 100);
        subtotal += dict.subtotal;
    });
    //Asignamos los valores a los campos
    compra.items.subtotal = subtotal - ivaCalculado;
    compra.items.iva = ivaCalculado;
    compra.items.percepcion = percepcion;
    if (percepcionPorcentaje > 0) {
        compra.items.percepcion = compra.items.subtotal * (percepcionPorcentaje / 100);
        compra.items.total = compra.items.subtotal + compra.items.iva + compra.items.percepcion;
    } else {
        compra.items.percepcion = percepcion;
        compra.items.total = compra.items.subtotal + compra.items.iva;
    }
    $('input[name="subtotal"]').val(compra.items.subtotal.toFixed(2));
    $('input[name="iva"]').val(compra.items.iva.toFixed(2));
    $('input[name="percepcion"]').val(compra.items.percepcion.toFixed(2));
    $('input[name="total"]').val(compra.items.total.toFixed(2));
};

//Funcion para buscar la percepcion del cliente
function searchPercepcion() {
    var id = $('select[name="proveedor"]').val();
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
        $('input[name="nroComprobante"]').val('');
        $('select[name="proveedor"]').val(null).trigger('change');
        $('select[name="medioPago"]').val(null).trigger('change');
        $('input[name="searchProductos"]').attr('disabled', true);
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
        //Buscamos si el Proveedor tiene percepcion
        searchPercepcion();
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
                compra.items.productos = data;
                //actualizamos el listado de productos
                compra.listProductos();
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

    //Inicializamos los campos de tipo TOUCHSPIN
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
            error_action('Error', 'La fecha de compra no puede ser superior a la actual', function () {
                //pass
            }, function () {
                $('input[name="fecha"]').val(moment().format('DD-MM-YYYY'));
            });

        }
    });

//----------------------Buscamos si el Proveedor tiene Percepcion-----------------------------//
    $('select[name="proveedor"]').on('change', function () {
        var id = $('select[name="proveedor"]').val();
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
        } else {
            $('input[name="searchProductos"]').attr('disabled', true);
        }
    });

//------------------------------------MODAL PROVEEDORES----------------------------------------//
    //Boton Proveedor Modal Mostrar
    $('.btnAddProveedor').on('click', function () {
        $('#modalProveedor').modal('show');
    });

    //Al cerrar el Modal de Proveedor reseteamos los valores del formulario
    $('#modalProveedor').on('hidden.bs.modal', function (e) {
        //Reseteamos los input del Modal
        $('#formProveedor').trigger('reset');
        //Reseteamos los Select2 del Modal
        $(".condicionIvaFormProveedor").val('').trigger('change.select2');
        $(".localidadFormProveedor").val('').trigger('change.select2');
        $(".condicionPagoFormProveedor").val('').trigger('change.select2');
        var errorList = document.getElementById("errorListFormProveedor");
        errorList.innerHTML = '';
    });

    //CHECKBOX Cta Cte
    $('#ctaCte').on('click', function () {
        if (this.checked) {
            $('input[name="plazoCtaCte"]').attr('disabled', false);
            $('input[name="plazoCtaCte"]').attr('readonly', false);
            $('input[name="plazoCtaCte"]').trigger("touchspin.updatesettings", {min: 0});
            $('input[name="plazoCtaCte"]').trigger("touchspin.updatesettings", {max: 1000000});
        } else {
            $('input[name="plazoCtaCte"]').val(0);
            $('input[name="plazoCtaCte"]').attr('readonly', true);
            $('input[name="plazoCtaCte"]').trigger("touchspin.updatesettings", {min: 0});
            $('input[name="plazoCtaCte"]').trigger("touchspin.updatesettings", {max: 0});
        }
    });

    //Validamos EMAIL CORRECTO en el formulario de Proveedor
    $("#email").on('focusout', function (e) {
        var btn = document.getElementById('btnAddProveedor');
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
    $("#cuit").validate();
    $("#localidad").validate();
    $("#direccion").validate();
    $("#telefono").validate();
    $("#email").validate();

    //Funcion Mostrar Errores del Formulario Proveedor
    function message_error_proveedor(obj) {
        var errorList = document.getElementById("errorListFormProveedor");
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

    //Creamos un nuevo Proveedor desde el Modal
    $('#formProveedor').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_proveedor');
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
                $('select[name="proveedor"]').append(newOption).trigger('change');
                $('#modalProveedor').modal('hide');
            } else {
                message_error_proveedor(data.error);
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
                compra.addProducto(ui.item);
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
                    compra.addProducto(item);
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
                compra.items.productos.splice(tr.row, 1);
                //Actualizamos el Listado
                compra.listProductos();
            }, function () {
            });
        })
        //evento cambiar renglon (cantidad) del detalle
        .on('change', 'input[name="cantidad"]', function () {
            //asignamos a una variable la cantidad, en la posicion actual
            var cant = parseInt($(this).val());
            //Obtenemos la posicion del elemento a modificar dentro del Datatables
            var tr = tablaProductos.cell($(this).closest('td, li')).index();
            compra.items.productos[tr.row].cantidad = cant;
            //Actualizamos los importes
            calcular_importes();
            //Actualizamos el importe de subtotal en la Posicion correspondiente en cada modificación
            $('td:eq(4)', tablaProductos.row(tr.row).node()).html('$' + compra.items.productos[tr.row].subtotal.toFixed(2));
        })
        //evento cambiar renglon (cantidad) del detalle
        .on('change', 'input[name="costo"]', function () {
            //asignamos a una variable el costo, en la posicion actual
            var costo = parseFloat($(this).val());
            //Obtenemos la posicion del elemento a modificar dentro del Datatables
            var tr = tablaProductos.cell($(this).closest('td, li')).index();
            compra.items.productos[tr.row].costo = costo;
            //Actualizamos los importes
            calcular_importes();
            //Actualizamos el importe de subtotal en la Posicion correspondiente en cada modificación
            $('td:eq(4)', tablaProductos.row(tr.row).node()).html('$' + compra.items.productos[tr.row].subtotal.toFixed(2));
        });

//Borrar desde el boton de busqueda de productos
    $('.btnClearSearchProductos').on('click', function () {
        $('input[name="searchProductos"]').val('').focus();
    });
//Borrar todos los productos
    $('.btnRemoveAllProductos').on('click', function () {
        if (compra.items.productos.length === 0) return false;
        //Ejecutar la Funcion de Confirmacion
        confirm_action('Confirmación', '¿Estas seguro de eliminar todos los registros?', function () {
            //removemos el listado de productos
            compra.items.productos = [];
            //Actualizamos el Listado
            compra.listProductos();
        }, function () {
        });
    });

//------------------------------------SUBMIT COMPRA----------------------------------------//
    // Submit COMPRA
    $('#compraForm').on('submit', function (e) {
        e.preventDefault();
        if (compra.items.productos.length === 0 ) {
            error_action('Error', 'Debe al menos tener un producto en sus detalle', function () {
                //pass
            }, function () {
                //pass
            });
        } else {
            confirm_action('Confirmación', '¿Estas seguro de realizar la siguiente acción?', function () {
                    //realizamos la compra mediante Ajax
                    compra.items.tipoComprobante = $('select[name="tipoComprobante"]').val();
                    compra.items.nroComprobante = $('input[name="nroComprobante"]').val();
                    compra.items.medioPago = $('select[name="medioPago"]').val();
                    compra.items.fecha = moment(moment($('input[name="fecha"]').val(), 'DD-MM-YYYY')).format('YYYY-MM-DD');
                    compra.items.proveedor = $('select[name="proveedor"]').val();
                    var parameters = new FormData();
                    //Pasamos la accion ADD
                    parameters.append('action', $('input[name="action"]').val());
                    //Agregamos la estructura de Compra con los detalles correspondientes
                    parameters.append('compra', JSON.stringify(compra.items));
                    //Bloque AJAX COMPRA
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
                                confirm_action('Notificación', '¿Desea imprimir la nota de compra?', function () {
                                    window.open('/compras/pdf/' + data.id + '/', '_blank');
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
    })
    ;
})
;

