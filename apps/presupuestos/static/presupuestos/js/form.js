var tablaProductos;
var tablaServicios;
var percepcionPorcentaje = 0.00;
//Definimos una estructura en JS para crear el PRESUPUESTO
var presupuesto = {
    items: {
        usuario: '',
        fecha: '',
        validez: '',
        cliente: '',
        modelo: '',
        observaciones: '',
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
            data: presupuesto.items.productos,
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
};

//Funcion para validar que el email tenga el formato correcto
function isValidEmail(mail) {
    return /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$/.test(mail);
};

//Funcion para Calcular los importes
function calcular_importes() {
    //Inicializamos variables para calcular importes
    var subtotal = 0.00;
    var ivaCalculado = 0.00;
    var percepcion = percepcionPorcentaje;
    //Recorremos el Array de productos para ir actualizando los importes
    $.each(presupuesto.items.productos, function (pos, dict) {
        dict.pos = pos;
        dict.subtotal = dict.cantidad * parseFloat(dict.precioVenta);
        ivaCalculado += dict.subtotal * (dict.iva.iva / 100);
        subtotal += dict.subtotal;
    });
    //Recorremos el Array de servicios para ir actualizando los importes
    $.each(presupuesto.items.servicios, function (pos, dict) {
        dict.pos = pos;
        dict.subtotal = dict.cantidad * parseFloat(dict.precioVenta);
        ivaCalculado += dict.subtotal * (dict.iva.iva / 100);
        subtotal += dict.subtotal;
    });
    //Asignamos los valores a los campos
    presupuesto.items.subtotal = subtotal - ivaCalculado;
    presupuesto.items.iva = ivaCalculado;
    presupuesto.items.percepcion = percepcion;
    if (percepcionPorcentaje > 0) {
        presupuesto.items.percepcion = presupuesto.items.subtotal * (percepcionPorcentaje / 100);
        presupuesto.items.total = presupuesto.items.subtotal + presupuesto.items.iva + presupuesto.items.percepcion;
    } else {
        presupuesto.items.percepcion = percepcion;
        presupuesto.items.total = presupuesto.items.subtotal + presupuesto.items.iva;
    }
    $('input[name="subtotal"]').val(presupuesto.items.subtotal.toFixed(2));
    $('input[name="iva"]').val(presupuesto.items.iva.toFixed(2));
    $('input[name="percepcion"]').val(presupuesto.items.percepcion.toFixed(2));
    $('input[name="total"]').val(presupuesto.items.total.toFixed(2));
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
    $('select[name="cliente"]').val(null).trigger('change');
    $('select[name="marca"]').val(null).trigger('change');
    $('select[name="modelo"]').val(null).trigger('change');
    $('select[name="selectPlantilla"]').val(null).trigger('change');
    //Inicializamos los campos de tipo TOUCHSPIN
    $("input[name='validez']").TouchSpin({
        min: 1,
        max: 1000000,
        step: 1,
        boostat: 5,
        maxboostedstep: 10,
    });
    var accion = $('input[name="action"]').val();
    if (accion === 'add') {
        $('input[name="subtotalProductos"]').val('0.00');
        $('input[name="subtotalServicios"]').val('0.00');
        $('input[name="iva"]').val('0.00');
        $('input[name="percepcion"]').val('0.00');
        $('input[name="total"]').val('0.00');
        $('input[name="descripcion"]').val('');
        $('select[name="cliente"]').val(null).trigger('change');
        $('select[name="marca"]').val(null).trigger('change');
        $('select[name="modelo"]').val(null).trigger('change');
        $('select[name="selectPlantilla"]').val(null).trigger('change');
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
        //Buscamos si el cliente tiene percepcion
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
                //asignamos el detalle a la estructura
                presupuesto.items.productos = data;
                //actualizamos el listado de productos
                presupuesto.listProductos();
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
                //asignamos el detalle a la estructura
                presupuesto.items.servicios = data;
                //actualizamos el listado de productos
                presupuesto.listServicios();
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

    //Funcion Mostrar Errores del Formulario
    function message_error(obj, errorList) {
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

//----------------------Seleccionamos un MODELO-----------------------------//
    $('select[name="modelo"]').on('change', function () {
        var id = $('select[name="modelo"]').val();
        if (id !== null && id !== '' && id !== undefined) {
            $('input[name="searchProductos"]').attr('disabled', false);
            $('input[name="searchServicios"]').attr('disabled', false);
        } else {
            $('input[name="searchProductos"]').attr('disabled', true);
            $('input[name="searchServicios"]').attr('disabled', true);
        }
    });

//Select Anidado (Seleccionamos MODELO y cargamos los MODELOS de dicha MARCA)
    var select_modelos = $('select[name="modelo"]');
    $('.selectMarca').on('change', function () {
        var id = $(this).val();
        var options = '<option value="">---------</option>';
        if (id === '') {
            select_modelos.html(options);
            return false;
        }
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'search_modelos',
                'pk': id
            },
            dataType: 'json',
            success: function (data) {
                if (!data.hasOwnProperty('error')) {
                    //Volvemos a cargar los datos del Select2 solo que los datos (data) ingresados vienen por AJAX
                    select_modelos.html('').select2({
                        theme: "bootstrap4",
                        language: 'es',
                        data: data
                    });
                }
            }
        });
    });

//Select Anidado (Seleccionamos MODELO y cargamos las PLANTILLAS DE DICHO PRESUPUESTO)
    var select_plantillas = $('select[name="selectPlantilla"]');
    $('.selectModelo').on('change', function () {
        var id = $(this).val();
        var options = '<option value="">---------</option>';
        if (id === '') {
            select_plantillas.html(options);
            return false;
        }
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'search_plantillas',
                'pk': id
            },
            dataType: 'json',
            success: function (data) {
                if (!data.hasOwnProperty('error')) {
                    //Volvemos a cargar los datos del Select2 solo que los datos (data) ingresados vienen por AJAX
                    select_plantillas.html('').select2({
                        theme: "bootstrap4",
                        language: 'es',
                        data: data
                    });
                }
            }
        });
    });

//Cargamos al detalle de productos y servicios los datos de la PLANTILLA
    $('.selectPlantilla').on('change', function () {
        var id = $(this).val();
        if (id === '') {
            return false;
        } else {
            //Buscamos el detalle de los productos por ajax
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrftoken,
                    'action': 'get_detalle_productos',
                    'pk': id
                },
                dataType: 'json',
                success: function (data) {
                    //asignamos el detalle a la estructura
                    presupuesto.items.productos = data;
                    //actualizamos el listado de productos
                    presupuesto.listProductos();
                }
            });
            //Buscamos el detalle de los servicios por ajax
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrftoken,
                    'action': 'get_detalle_servicios',
                    'pk': id
                },
                dataType: 'json',
                success: function (data) {
                    //asignamos el detalle a la estructura
                    presupuesto.items.servicios = data;
                    //actualizamos el listado de productos
                    presupuesto.listServicios();
                }
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
        if ($('input[name="email"]').val().lenght == 0 || !$('input[name="email"]').val()) {
            //email vacio
            $('#errorEmail').attr("hidden", "");
            btn.disabled = false;
        } else {
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
        }
    });

    // VALIDAMOS LOS CAMPOS
    $("#razonSocial").validate();
    $("#condicionIVA").validate();
    $("#cuil").validate();
    $("#localidad").validate();
    $("#direccion").validate();
    $("#telefono").validate();

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
                presupuesto.addProducto(ui.item);
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
                    presupuesto.addProducto(item);
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
                presupuesto.items.productos.splice(tr.row, 1);
                //Actualizamos el Listado
                presupuesto.listProductos();
            }, function () {
            });
        })
        //evento cambiar renglon (cantidad) del detalle
        .on('change', 'input[name="cantidad"]', function () {
            //asignamos a una variable la cantidad, en la posicion actual
            var cant = parseInt($(this).val());
            //Obtenemos la posicion del elemento a modificar dentro del Datatables
            var tr = tablaProductos.cell($(this).closest('td, li')).index();
            presupuesto.items.productos[tr.row].cantidad = cant;
            //Actualizamos los importes
            calcular_importes();
            //Actualizamos el importe de subtotal en la Posicion correspondiente en cada modificación
            $('td:eq(4)', tablaProductos.row(tr.row).node()).html('$' + presupuesto.items.productos[tr.row].subtotal.toFixed(2));
        });

//Borrar desde el boton de busqueda de productos
    $('.btnClearSearchProductos').on('click', function () {
        $('input[name="searchProductos"]').val('').focus();
    });
//Borrar todos los productos
    $('.btnRemoveAllProductos').on('click', function () {
        if (presupuesto.items.productos.length === 0) return false;
        //Ejecutar la Funcion de Confirmacion
        confirm_action('Confirmación', '¿Estas seguro de eliminar todos los registros?', function () {
            //removemos el listado de productos
            presupuesto.items.productos = [];
            //Actualizamos el Listado
            presupuesto.listProductos();
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
            presupuesto.addServicio(ui.item);
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
                    presupuesto.addServicio(item);
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
                presupuesto.items.servicios.splice(tr.row, 1);
                //Actualizamos el Listado
                presupuesto.listServicios();
            }, function () {
            });
        })
        //evento cambiar renglon (cantidad) del detalle
        .on('change', 'input[name="cantidad"]', function () {
            //asignamos a una variable la cantidad, en la posicion actual
            var cant = parseInt($(this).val());
            //Obtenemos la posicion del elemento a modificar dentro del Datatables
            var tr = tablaServicios.cell($(this).closest('td, li')).index();
            presupuesto.items.servicios[tr.row].cantidad = cant;
            //Actualizamos los importes
            calcular_importes();
            //Actualizamos el importe de subtotal en la Posicion correspondiente en cada modificación
            $('td:eq(4)', tablaServicios.row(tr.row).node()).html('$' + presupuesto.items.servicios[tr.row].subtotal.toFixed(2));
        });

    //Borrar desde el boton de busqueda de productos
    $('.btnClearSearchServicios').on('click', function () {
        $('input[name="searchServicios"]').val('').focus();
    });

    //Borrar todos los Servicios
    $('.btnRemoveAllServicios').on('click', function () {
        if (presupuesto.items.servicios.length === 0) return false;
        //Ejecutar la Funcion de Confirmacion
        confirm_action('Confirmación', '¿Estas seguro de eliminar todos los registros?', function () {
            //removemos el listado de servicios
            presupuesto.items.servicios = [];
            //Actualizamos el Listado
            presupuesto.listServicios();
        }, function () {
        });
    });

//------------------------------------SUBMIT PRESUPUESTO----------------------------------------//
    // Submit PRESUPUESTO
    $('#presupuestoForm').on('submit', function (e) {
        e.preventDefault();
        if (presupuesto.items.productos.length === 0 && presupuesto.items.servicios.length === 0) {
            error_action('Error', 'Debe al menos tener un producto o servicio en sus detalles', function () {
                //pass
            }, function () {
                //pass
            });
        } else {
            confirm_action('Confirmación', '¿Estas seguro de realizar la siguiente acción?', function () {
                    //realizamos la creacion del Presupuesto mediante Ajax
                    presupuesto.items.modelo = $('select[name="modelo"]').val();
                    presupuesto.items.descripcion = $('input[name="descripcion"]').val();
                    var parameters = new FormData();
                    //Pasamos la accion ADD
                    parameters.append('action', $('input[name="action"]').val());
                    //Agregamos la estructura de Presupuesto con los detalles correspondientes
                    parameters.append('presupuestoBase', JSON.stringify(presupuesto.items));
                    //Bloque AJAX Presupuesto
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
                                confirm_action('Notificación', '¿Desea imprimir el Presupuesto Base?', function () {
                                    window.open('/presupuestosBase/pdf/' + data.id + '/', '_blank');
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

