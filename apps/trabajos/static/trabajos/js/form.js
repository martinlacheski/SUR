var renglon;
var tablaProductos;
var tablaServicios;
var percepcionPorcentaje = 0.00;
//Definimos una estructura en JS para crear el TRABAJO
var trabajo = {
    items: {
        usuario: '',
        fichaTrabajo: '',
        fechaEntrada: '',
        fechaSalida: '',
        cliente: '',
        modelo: '',
        usuarioAsignado: '',
        subtotal: 0.00,
        iva: 0.00,
        percepcion: 0.00,
        total: 0.00,
        prioridad: '',
        estadoTrabajo: '',
        observaciones: '',
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
            data: trabajo.items.productos,
            columns: [
                {"data": "id"}, //Para el boton eliminar
                {"data": "descripcion"},
                {"data": "precioVenta"},
                {"data": "cantidad"},
                {"data": "subtotal"},
                {"data": "id"}, //Para el boton actualizar
                {"data": "id"}, //Para el boton Observaciones
                {"data": "estado"},
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
                    targets: [-6],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="Text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
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
                        return '<a rel="update" class="btn btn-warning btn-xs btn-flat" style="color: black;" ><i class="fas fa-edit"></i></a>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="observaciones" class="btn btn-info btn-xs btn-flat" style="color: black;" ><i class="fas fa-search"></i></a>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    className: 'dt-body-center',
                    render: function (data, type, row) {
                        if (row.estado) {
                            return '<input type="checkbox" name="realizado" class="form-control-sm input-sm" checked>';
                        } else {
                            return '<input type="checkbox" name="realizado" class="form-control-sm input-sm">';
                        }
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
                {"data": "id"}, //Para el boton actualizar
                {"data": "id"}, //Para el boton observaciones
                {"data": "estado"},
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
                    targets: [-6],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="Text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
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
                        return '<a rel="update" class="btn btn-warning btn-xs btn-flat" style="color: black;" ><i class="fas fa-edit"></i></a>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="observaciones" class="btn btn-info btn-xs btn-flat" style="color: black;" ><i class="fas fa-search"></i></a>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if (row.estado) {
                            return '<input type="checkbox" name="realizado" class="form-control-sm input-sm" checked>';
                        } else {
                            return '<input type="checkbox" name="realizado" class="form-control-sm input-sm">';
                        }
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

//Funcion para validar que el CUIT sea válido
function isValidCuit(cuit) {
    //si el largo del cuit es incorrecto salir de la funcion
    if (cuit.length != 11) return 0;
    var rv = false;
    var resultado = 0;
    var cuit_nro = cuit.replace("-", "");
    var codes = "6789456789";
    var cuit_long = parseInt(cuit_nro);
    var verificador = parseInt(cuit_nro[cuit_nro.length - 1]);
    var x = 0;
    while (x < 10) {
        var digitoValidador = parseInt(codes.substring(x, x + 1));
        if (isNaN(digitoValidador)) digitoValidador = 0;
        var digito = parseInt(cuit_nro.substring(x, x + 1));
        if (isNaN(digito)) digito = 0;
        var digitoValidacion = digitoValidador * digito;
        resultado += digitoValidacion;
        x++;
    }
    resultado = resultado % 11;
    rv = (resultado == verificador);
    return rv;
};

//Funcion para Calcular los importes
function calcular_importes() {
    //Inicializamos variables para calcular importes
    var subtotal = 0.00;
    var ivaCalculado = 0.00;
    var percepcion = percepcionPorcentaje;
    var subtotalProductos = 0.00;
    var subtotalServicios = 0.00;
    //Recorremos el Array de productos para ir actualizando los importes
    $.each(trabajo.items.productos, function (pos, dict) {
        dict.pos = pos;
        dict.subtotal = dict.cantidad * parseFloat(dict.precioVenta);
        ivaCalculado += dict.subtotal * (dict.iva.iva / 100);
        subtotalProductos += dict.subtotal;
        subtotal += dict.subtotal;
    });
    //Recorremos el Array de servicios para ir actualizando los importes
    $.each(trabajo.items.servicios, function (pos, dict) {
        dict.pos = pos;
        dict.subtotal = dict.cantidad * parseFloat(dict.precioVenta);
        ivaCalculado += dict.subtotal * (dict.iva.iva / 100);
        subtotalServicios += dict.subtotal;
        subtotal += dict.subtotal;
    });

    //Asignamos los valores a los campos
    trabajo.items.subtotal = subtotal - ivaCalculado;
    trabajo.items.iva = ivaCalculado;
    trabajo.items.percepcion = percepcion;
    if (percepcionPorcentaje > 0) {
        trabajo.items.percepcion = trabajo.items.subtotal * (percepcionPorcentaje / 100);
        trabajo.items.total = trabajo.items.subtotal + trabajo.items.iva + trabajo.items.percepcion;
    } else {
        trabajo.items.percepcion = percepcion;
        trabajo.items.total = trabajo.items.subtotal + trabajo.items.iva;
    }
    $('input[name="subtotalProductos"]').val(subtotalProductos.toFixed(2));
    $('input[name="subtotalServicios"]').val(subtotalServicios.toFixed(2));
    $('input[name="iva"]').val(trabajo.items.iva.toFixed(2));
    $('input[name="percepcion"]').val(trabajo.items.percepcion.toFixed(2));
    $('input[name="total"]').val(trabajo.items.total.toFixed(2));
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

$(document).ready(function () {
    $('select[name="marca"]').val(null).trigger('change');
    //Inicializamos los Select2
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
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
        $('#fechaEntrada').datetimepicker({
            format: 'DD-MM-YYYY',
            date: moment(),
            locale: 'es',
            // minDate: moment(),
            maxDate: moment(),
        });
        // Buscamos el usuario mas desocupado
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'get_mas_desocupado',
            },
            dataType: 'json',
            success: function (data) {
                // Colocamos en el select el usuario mas desocupado
                $('select[name="usuarioAsignado"]').html('').select2({
                    theme: "bootstrap4",
                    language: 'es',
                    data: data
                });
            }
        });
    } else if (accion === 'express') {
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
        $('#fechaEntrada').datetimepicker({
            format: 'DD-MM-YYYY',
            date: moment(),
            locale: 'es',
            maxDate: moment(),
        });
    } else {
        $('#fechaEntrada').datetimepicker({
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
                trabajo.items.productos = data;
                //actualizamos el listado de productos
                trabajo.listProductos();
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
                trabajo.items.servicios = data;
                //actualizamos el listado de productos
                trabajo.listServicios();
            }
        });
    }
})
;

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
    $('input[name="fechaEntrada"]').on('blur', function () {
        var fecha = $('input[name="fechaEntrada"]').val();
        var now = moment().format('DD-MM-YYYY');
        if (fecha > now) {
            error_action('Error', 'La fecha de entrada no puede ser superior a la actual', function () {
                //pass
            }, function () {
                $('input[name="fechaEntrada"]').val(moment().format('DD-MM-YYYY'));
            });

        }
    });

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

//Select Anidado (Seleccionamos MODELO y cargamos las PLANTILLAS DE DICHO TRABAJO)
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
                    trabajo.items.productos = data;
                    //Agregamos el estado a FALSE por cada Producto
                    for (var i = 0; i < trabajo.items.productos.length; i++) {
                        trabajo.items.productos[i].estado = false
                    }
                    //actualizamos el listado de productos
                    trabajo.listProductos();
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
                    trabajo.items.servicios = data;
                    //Agregamos el estado a FALSE por cada Servicio
                    for (var i = 0; i < trabajo.items.servicios.length; i++) {
                        trabajo.items.servicios[i].estado = false
                    }
                    //actualizamos el listado de productos
                    trabajo.listServicios();
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

    //Validamos CUIT CORRECTO
    $("#cuil").on('focusout', function (e) {
        var btn = document.getElementById('btnAddCliente');
        if ($('input[name="cuil"]').val().lenght == 0 || !$('input[name="cuil"]').val()) {
            //cuit vacio
            $('#errorCuit').attr("hidden", "");
            btn.disabled = false;
        } else {
            var check = isValidCuit($('input[name="cuil"]').val());
            if (check == false) {
                //alert('Dirección de correo electrónico no válido');
                $("#errorCuit").removeAttr("hidden");
                btn.disabled = true;
                $("#cuil").focus();
            } else {
                $('#errorCuit').attr("hidden", "");
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
    //Agregamos el Producto al Trabajo
    $('#tablaSearchProductos tbody')
        .on('click', 'a[rel="addProducto"]', function () {
            //Asignamos a una variable el renglon que necesitamos
            var tr = tablaSearchProductos.cell($(this).closest('td, li')).index();
            //Asignamos a una variable el producto en base al renglon
            var producto = tablaSearchProductos.row(tr.row).data();
            producto.cantidad = 1;
            producto.subtotal = 0.00;
            producto.estado = false;
            producto.observaciones = "";
            trabajo.addProducto(producto);
            //Una vez cargado el producto, sacamos del listado del Datatables
            tablaSearchProductos.row($(this).parents('tr')).remove().draw();
        });

//------------------------------------MODAL PRODUCTOS----------------------------------------//

    ///Boton Agregar Producto Mostrar Modal
    $('.btnAddProducto').on('click', function () {
        $('#modalProducto').modal('show');
        //Inicializamos SELECT2
        $('.ivaProducto').select2({
            theme: "bootstrap4",
            language: 'es'
        });
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
        max: 1000,
        step: 0.1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    });
    $('.precioVenta').TouchSpin({
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
                ui.item.estado = false;
                ui.item.observaciones = "";
                trabajo.addProducto(ui.item);
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
                    item.estado = false;
                    item.observaciones = "";
                    trabajo.addProducto(item);
                    $('input[name="searchProductos"]').val('');
                    $('input[name="searchProductos"]').focus();
                } else {
                    //error_action('Error', 'No existe el producto con el código ingresado', function () {
                    confirm_action('Error', 'No existe el producto, ¿Desea registrarlo?', function () {
                        $('#modalProducto').modal('show');
                        //Inicializamos SELECT2
                        $('.ivaProducto').select2({
                            theme: "bootstrap4",
                            language: 'es'
                        });
                        $('input[name="searchProductos"]').val('');
                        $('input[name="searchProductos"]').focus();
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
    //Borrar desde el boton de busqueda de productos
    $('.btnClearSearchProductos').on('click', function () {
        $('input[name="searchProductos"]').val('').focus();
    });
    //Borrar todos los productos
    $('.btnRemoveAllProductos').on('click', function () {
        if (trabajo.items.productos.length === 0) return false;
        //Ejecutar la Funcion de Confirmacion
        confirm_action('Confirmación', '¿Estas seguro de eliminar todos los registros?', function () {
            //removemos el listado de productos
            trabajo.items.productos = [];
            //Actualizamos el Listado
            trabajo.listProductos();
        }, function () {
        });
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
                trabajo.items.productos.splice(tr.row, 1);
                //Actualizamos el Listado
                trabajo.listProductos();
            }, function () {
            });
        })
        //evento cambiar renglon (cantidad) del detalle
        .on('change', 'input[name="cantidad"]', function () {
            //asignamos a una variable la cantidad, en la posicion actual
            var cant = parseInt($(this).val());
            //Obtenemos la posicion del elemento a modificar dentro del Datatables
            var tr = tablaProductos.cell($(this).closest('td, li')).index();
            trabajo.items.productos[tr.row].cantidad = cant;
            //Actualizamos los importes
            calcular_importes();
            //Actualizamos el importe de subtotal en la Posicion correspondiente en cada modificación
            $('td:eq(4)', tablaProductos.row(tr.row).node()).html('$' + trabajo.items.productos[tr.row].subtotal.toFixed(2));
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
            $('input[name="actualizarSubcategoriaProducto"]').val(prod.subcategoria.nombre);
            $('input[name="actualizarDescripcionProducto"]').val(prod.descripcion);
            $('input[name="actualizarCostoProducto"]').val(prod.costo)
                .TouchSpin({
                    min: 0,
                    max: 1000000,
                    step: 0.1,
                    decimals: 2,
                    boostat: 5,
                    maxboostedstep: 10,
                    postfix: '$'
                });
            $('input[name="actualizarUtilidadProducto"]').val(prod.utilidad)
                .TouchSpin({
                    min: 0,
                    max: 1000,
                    step: 0.1,
                    decimals: 2,
                    boostat: 5,
                    maxboostedstep: 10,
                    postfix: '%'
                });
            $('input[name="actualizarIvaProducto"]').val(prod.iva.iva);
            $('input[name="actualizarPrecioVentaProducto"]').val(prod.precioVenta)
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
        })
        //Evento Ingresar Observaciones del Producto del detalle
        .on('click', 'a[rel="observaciones"]', function () {
            //Asignamos a una variable el renglon que necesitamos
            var tr = tablaProductos.cell($(this).closest('td, li')).index();
            renglon = tr.row;
            //Asignamos a una variable el producto en base al renglon
            var prod = tablaProductos.row(tr.row).data();
            //Cargamos los valores del Producto en el modal
            $('input[name="idObservacionProductoUpdate"]').val(prod.id);   //INPUT HIDDEN ID PRODUCTO
            $('input[name="observacionDescripcionProducto"]').val(prod.descripcion);
            $('input[name="observacionProducto"]').val(trabajo.items.productos[tr.row].observaciones);
            $('#modalObservacionesProducto').modal('show');
        })
        //evento cambiar renglon (cantidad) del detalle
        .on('change', 'input[name="realizado"]', function () {
            //asignamos a una variable el Estado de Realizado, en la posicion actual
            if (!this.checked) {
                var estado = false;
            } else {
                var estado = true;
            }
            //Obtenemos la posicion del elemento a modificar dentro del Datatables
            var tr = tablaProductos.cell($(this).closest('td, li')).index();
            trabajo.items.productos[tr.row].estado = estado;
        });

    //------------------------------------MODAL ACTUALIZAR PRECIO PRODUCTOS----------------------------------------//
    //EN MODAL ACTUALIZAR PRECIO PRODUCTO
    // Metodo para calcular el precio en base a los tres posibles cambios (COSTO UTILIDAD y Precio Venta)
    $('input[name="actualizarCostoProducto"]').on('change', function () {
        calcularPrecioActualizacion();
    });
    $('input[name="actualizarUtilidadProducto"]').on('change', function () {
        calcularPrecioActualizacion();
    });
    $('input[name="actualizarPrecioVentaProducto"]').on('change', function () {
        calcularUtilidadActualizacion();
    });

    //Funcion para calcular el precio entre COSTO UTILIDAD e IVA
    function calcularPrecioActualizacion() {
        var iva = $('input[name="actualizarIvaProducto"]').val();
        var costo = $('input[name="actualizarCostoProducto"]').val();
        var utilidad = $('input[name="actualizarUtilidadProducto"]').val();
        utilidad = (utilidad / 100) + 1;
        iva = (iva / 100) + 1;
        var precio = (costo * utilidad * iva);
        $('input[name="actualizarPrecioVentaProducto"]').val(precio.toFixed(2));
    }

    //Funcion para calcular el precio entre COSTO IVA y TOTAL
    function calcularUtilidadActualizacion() {
        var iva = $('input[name="actualizarIvaProducto"]').val();
        var costo = $('input[name="actualizarCostoProducto"]').val();
        var total = $('input[name="actualizarPrecioVentaProducto"]').val();
        iva = (iva / 100) + 1;
        var precio = (((total / iva) / costo) - 1) * 100;
        $('input[name="actualizarUtilidadProducto"]').val(precio.toFixed(2));
    }

    //Actualizamos el precio del PRODUCTO desde el Modal
    $('#formPrecioProducto').on('submit', function (e) {
        e.preventDefault();
        confirm_action('Confirmación', '¿Estas seguro de realizar la siguiente acción?', function () {
            var id = $('input[name="idProductoUpdate"]').val();
            var costo = $('input[name="actualizarCostoProducto"]').val();
            var utilidad = $('input[name="actualizarUtilidadProducto"]').val();
            var precioVenta = $('input[name="actualizarPrecioVentaProducto"]').val();
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
                    trabajo.listProductos();
                    $('#modalPrecioProducto').modal('hide');

                } else {
                    message_error_precio_producto(data.error);
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
            }).always(function (data) {
            });
            //Asignamos a una variable el producto en base al renglon
            var prod = trabajo.items.productos[renglon];
            //actualizamos el costo y subtotal del producto en el array
            prod.precioVenta = precioVenta;
            prod.subtotal = precioVenta * prod.cantidad;
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

//------------------------------------MODAL Ingresar Observacion Producto----------------------------------------//
    //Ingresamos una observacion del PRODUCTO desde el Modal
    $('#formObservacionesProducto').on('submit', function (e) {
        e.preventDefault();
        //Asignamos a una variable la observacion del Producto
        var observacion = $('input[name="observacionProducto"]').val();
        //Asignamos a una variable el producto en base al renglon
        var prod = trabajo.items.productos[renglon];
        //ingresamos la observacion
        prod.observaciones = observacion;
        $('#modalObservacionesProducto').modal('hide');
    });
    //Al cerrar el Modal de Productos reseteamos los valores del formulario
    $('#modalObservacionesProducto').on('hidden.bs.modal', function (e) {
        //Reseteamos los input del Modal
        $('#formObservacionesProducto').trigger('reset');
        var errorList = document.getElementById("errorListformObservacionesProducto");
        errorList.innerHTML = '';
    });

//------------------------------------MODAL Buscar SERVICIOS----------------------------------------//
    //Boton Buscar Servicios Mostrar Modal
    $('.btnSearchServicios').on('click', function () {
        tablaSearchServicios = $('#tablaSearchServicios').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrftoken,
                    'action': 'search_all_servicios',
                },
                dataSrc: ""
            },
            columns: [
                {"data": "descripcion"},
                {"data": "precioVenta"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
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
                        var buttons = '<a rel="addServicio" class="btn btn-success btn-xs btn-flat"><i class="fas fa-plus"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
        $('#modalSearchServicios').modal('show');
    });
    //Agregamos el servicio al Trabajo
    $('#tablaSearchServicios tbody')
        .on('click', 'a[rel="addServicio"]', function () {
            //Asignamos a una variable el renglon que necesitamos
            var tr = tablaSearchServicios.cell($(this).closest('td, li')).index();
            //Asignamos a una variable el servicio en base al renglon
            var servicio = tablaSearchServicios.row(tr.row).data();
            servicio.cantidad = 1;
            servicio.subtotal = 0.00;
            servicio.observaciones = "";
            servicio.estado = false;
            trabajo.addServicio(servicio);
            //Una vez cargado el producto, sacamos del listado del Datatables
            tablaSearchServicios.row($(this).parents('tr')).remove().draw();
        });
//-----------------------------------MODAL SERVICIOS----------------------------------------//
    ///Boton Agregar Servicio Mostrar Modal
    $('.btnAddServicio').on('click', function () {
        $('#modalServicio').modal('show');
        //Inicializamos SELECT2
        $('.ivaServicio').select2({
            theme: "bootstrap4",
            language: 'es'
        });
    });
    //Inicializamos los campos de tipo TOUCHSPIN
    $("input[name='costoServicio']").TouchSpin({
        min: 0,
        max: 1000000,
        step: 0.1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '$'
    });

    //Al cerrar el Modal de Servicios reseteamos los valores del formulario
    $('#modalServicio').on('hidden.bs.modal', function (e) {
        //Reseteamos los input del Modal
        $('#formServicio').trigger('reset');
        //Reseteamos los Select2 del Modal
        $(".ivaServicio").val('').trigger('change.select2');
        var errorList = document.getElementById("errorListFormServicio");
        errorList.innerHTML = '';
    });
    //Metodo para calcular el precio en base a los posibles cambios (COSTO e IVA)
    $('input[name="costoServicio"]').on('change', function () {
        calcularPrecioServicio();
    });
    $('.ivaServicio').on('change', function () {
        calcularPrecioServicio();
    });

    //Funcion para calcular el precio entre COSTO e IVA
    function calcularPrecioServicio() {
        var id = $('.ivaServicio').val();
        var iva = 0;
        var costo = $('.costoServicio').val();
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
                    var precio = (costo * iva);
                    $('.precioVentaServicio').val(precio.toFixed(2));
                }
            }
        });
        if (iva > 0) {
            var precio = (costo * iva);
            $('.precioVentaServicio').val(precio.toFixed(2));
        }
    }

    //Funcion Mostrar Errores del Formulario
    function message_error_servicio(obj) {
        var errorList = document.getElementById("errorListFormServicio");
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

    //Hacemos el envio del Formulario mediante AJAX
    $("#formServicio").submit(function (e) {
        // VALIDACION DE LOS CAMPOS
        $("#descripcionServicio").validate();
        $("#codigoServicio").validate();
        $("#costoServicio").validate();
        $("#ivaServicio").validate();
        $("#precioVentaServicio").validate();
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_servicio');
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
                $('#modalServicio').modal('hide');
            } else {
                message_error_servicio(data.error);
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
        }).always(function (data) {
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
            ui.item.observaciones = "";
            ui.item.estado = false;
            trabajo.addServicio(ui.item);
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
                    item.estado = false;
                    item.observaciones = "";
                    trabajo.addServicio(item);
                    $('input[name="searchServicios"]').val('');
                    $('input[name="searchServicios"]').focus();
                } else {
                    //error_action('Error', 'No existe el servicio con el código ingresado', function () {
                    confirm_action('Error', 'No existe el servicio, ¿Desea registrarlo?', function () {
                        $('#modalServicio').modal('show');
                        //Inicializamos SELECT2
                        $('.ivaServicio').select2({
                            theme: "bootstrap4",
                            language: 'es'
                        });
                        $('input[name="searchServicios"]').val('');
                        $('input[name="searchServicios"]').focus();
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
    //Borrar desde el boton de busqueda de Servicios
    $('.btnClearSearchServicios').on('click', function () {
        $('input[name="searchServicios"]').val('').focus();
    });
    //Borrar todos los Servicios
    $('.btnRemoveAllServicios').on('click', function () {
        if (trabajo.items.servicios.length === 0) return false;
        //Ejecutar la Funcion de Confirmacion
        confirm_action('Confirmación', '¿Estas seguro de eliminar todos los registros?', function () {
            //removemos el listado de servicios
            trabajo.items.servicios = [];
            //Actualizamos el Listado
            trabajo.listServicios();
        }, function () {
        });
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
                trabajo.items.servicios.splice(tr.row, 1);
                //Actualizamos el Listado
                trabajo.listServicios();
            }, function () {
            });
        })
        //evento cambiar renglon (cantidad) del detalle
        .on('change', 'input[name="cantidad"]', function () {
            //asignamos a una variable la cantidad, en la posicion actual
            var cant = parseInt($(this).val());
            //Obtenemos la posicion del elemento a modificar dentro del Datatables
            var tr = tablaServicios.cell($(this).closest('td, li')).index();
            trabajo.items.servicios[tr.row].cantidad = cant;
            //Actualizamos los importes
            calcular_importes();
            //Actualizamos el importe de subtotal en la Posicion correspondiente en cada modificación
            $('td:eq(4)', tablaServicios.row(tr.row).node()).html('$' + trabajo.items.servicios[tr.row].subtotal.toFixed(2));
        })
        .on('click', 'a[rel="update"]', function () {
            //Asignamos a una variable el renglon que necesitamos
            var tr = tablaServicios.cell($(this).closest('td, li')).index();
            renglon = tr.row;
            //Asignamos a una variable el producto en base al renglon
            var serv = tablaServicios.row(tr.row).data();
            //Cargamos los valores del Producto en el modal
            $('input[name="idServicioUpdate"]').val(serv.id);   //INPUT HIDDEN ID PRODUCTO
            $('input[name="actualizarDescripcionServicio"]').val(serv.descripcion);
            $('input[name="actualizarCostoServicio"]').val(serv.costo)
                .TouchSpin({
                    min: 0,
                    max: 1000000,
                    step: 0.1,
                    decimals: 2,
                    boostat: 5,
                    maxboostedstep: 10,
                    postfix: '$'
                });
            $('input[name="actualizarIvaServicio"]').val(serv.iva.iva);
            $('input[name="actualizarPrecioVentaServicio"]').val(serv.precioVenta)
                .TouchSpin({
                    min: 0,
                    max: 1000000,
                    step: 0.1,
                    decimals: 2,
                    boostat: 5,
                    maxboostedstep: 10,
                    postfix: '$'
                });
            $('#modalPrecioServicio').modal('show');
        })
        //Evento Ingresar Observaciones del Servicio del detalle
        .on('click', 'a[rel="observaciones"]', function () {
            //Asignamos a una variable el renglon que necesitamos
            var tr = tablaServicios.cell($(this).closest('td, li')).index();
            renglon = tr.row;
            //Asignamos a una variable el Servicio en base al renglon
            var serv = tablaServicios.row(tr.row).data();
            //Cargamos los valores del Servicio en el modal
            $('input[name="idObservacionServicioUpdate"]').val(serv.id);   //INPUT HIDDEN ID SERVICIO
            $('input[name="observacionDescripcionServicio"]').val(serv.descripcion);
            $('input[name="observacionServicio"]').val(trabajo.items.servicios[tr.row].observaciones);
            $('#modalObservacionesServicio').modal('show');
        })
        //evento cambiar renglon (cantidad) del detalle
        .on('change', 'input[name="realizado"]', function () {
            //asignamos a una variable el Estado de Realizado, en la posicion actual
            if (!this.checked) {
                var estado = false;
            } else {
                var estado = true;
            }
            //Obtenemos la posicion del elemento a modificar dentro del Datatables
            var tr = tablaServicios.cell($(this).closest('td, li')).index();
            trabajo.items.servicios[tr.row].estado = estado;
        });
    //------------------------------------MODAL ACTUALIZAR PRECIO SERVICIOS----------------------------------------//
    //EN MODAL ACTUALIZAR PRECIO SERVICIO
    // Metodo para calcular el precio en base a los posibles cambios (COSTO y Precio Venta)
    $('input[name="actualizarCostoServicio"]').on('change', function () {
        calcularPrecioActualizacionServicio();
    });

    //Funcion para calcular el precio entre COSTO e IVA
    function calcularPrecioActualizacionServicio() {
        var iva = $('input[name="actualizarIvaServicio"]').val();
        var costo = $('input[name="actualizarCostoServicio"]').val();
        iva = (iva / 100) + 1;
        var precio = (costo * iva);
        $('input[name="actualizarPrecioVentaServicio"]').val(precio.toFixed(2));
    }

    //Actualizamos el precio del Servicio desde el Modal
    $('#formPrecioServicio').on('submit', function (e) {
        e.preventDefault();
        confirm_action('Confirmación', '¿Estas seguro de realizar la siguiente acción?', function () {
            var id = $('input[name="idServicioUpdate"]').val();
            var costo = $('input[name="actualizarCostoServicio"]').val();
            var precioVenta = $('input[name="actualizarPrecioVentaServicio"]').val();
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'update_precioServicio',
                    'pk': id,
                    'costo': costo,
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
                    trabajo.listServicios();
                    $('#modalPrecioServicio').modal('hide');

                } else {
                    message_error_precio_servicio(data.error);
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
            }).always(function (data) {
            });
            //Asignamos a una variable el Servicio en base al renglon
            var serv = trabajo.items.servicios[renglon];
            //actualizamos el costo y subtotal del Servicio en el array
            serv.precioVenta = precioVenta;
            serv.subtotal = precioVenta * serv.cantidad;
            //Actualizamos el valor del renglon del Datatables
            tablaServicios.row(renglon).data(serv).draw();
        }, function () {
            //pass
        });
    });

    //Funcion Mostrar Errores del Formulario Servicio
    function message_error_precio_servicio(obj) {
        var errorList = document.getElementById("errorListformPrecioServicio");
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

//------------------------------------MODAL Ingresar Observacion Servicio----------------------------------------//
    //Ingresamos una observacion del SERVICIO desde el Modal
    $('#formObservacionesServicio').on('submit', function (e) {
        e.preventDefault();
        //Asignamos a una variable la observacion del Servicio
        var observacion = $('input[name="observacionServicio"]').val();
        //Asignamos a una variable el Servicio en base al renglon
        var serv = trabajo.items.servicios[renglon];
        //ingresamos la observacion
        serv.observaciones = observacion;
        $('#modalObservacionesServicio').modal('hide');
    });

    //Al cerrar el Modal de Servicios reseteamos los valores del formulario
    $('#modalObservacionesServicio').on('hidden.bs.modal', function (e) {
        //Reseteamos los input del Modal
        $('#formObservacionesServicio').trigger('reset');
        var errorList = document.getElementById("errorListformObservacionesServicio");
        errorList.innerHTML = '';
    });
//------------------------------------SUBMIT TRABAJO----------------------------------------//
    // Submit TRABAJO
    $('#trabajoForm').on('submit', function (e) {
        e.preventDefault();
        var estadoServicio = true;
        var estadoProducto = true;
        var accion = $('input[name="action"]').val();
        //Recorremos los servicios para comprobar que ya se realizaron
        for (var i = 0; i < trabajo.items.servicios.length; i++) {
            if (trabajo.items.servicios[i].estado == false) {
                estadoServicio = false;
            }
        }
        //Recorremos los productos para comprobar que ya se realizaron
        for (var i = 0; i < trabajo.items.productos.length; i++) {
            if (trabajo.items.productos[i].estado == false) {
                estadoProducto = false;
            }
        }
        //Comprobamos que exista al menos un producto o un servicio
        if (trabajo.items.servicios.length === 0) {
            error_action('Error', 'Debe al menos tener un servicio en su detalle', function () {
                //pass
            }, function () {
                //pass
            });
            //Chequeamos que Si es la accion de Finalizar el trabajo, todos los servicios en el registro se hayan realizado
        } else if ((estadoServicio == false) && (accion == 'confirm')) {
            error_action('Error', 'Posee servicios sin realizarse, no se puede finalizar el trabajo', function () {
                //pass
            }, function () {
                //pass
            });
            //Chequeamos que Si es la accion de ENTREGAR el trabajo, todos los servicios y productos en el registro se hayan realizado
        } else if ((estadoProducto == false) && (estadoServicio == false) && (accion == 'deliver')) {
            error_action('Error', 'Posee productos y servicios  sin realizarse, no se puede entregar el trabajo', function () {
                //pass
            }, function () {
                //pass
            });
            //Chequeamos que Si es la accion de ENTREGAR el trabajo, todos los servicios y productos en el registro se hayan realizado
        } else if ((estadoProducto == false) && (accion == 'deliver')) {
            error_action('Error', 'Posee productos  sin realizarse, no se puede entregar el trabajo', function () {
                //pass
            }, function () {
                //pass
            });
            //Chequeamos que Si es la accion de ENTREGAR el trabajo, todos los servicios y productos en el registro se hayan realizado
        } else if ((estadoServicio == false) && (accion == 'deliver')) {
            error_action('Error', 'Posee servicios  sin realizarse, no se puede entregar el trabajo', function () {
                //pass
            }, function () {
                //pass
            });
        } else {
            confirm_action('Confirmación', '¿Estas seguro de realizar la siguiente acción?', function () {
                    //realizamos la creacion del Trabajo mediante Ajax
                    trabajo.items.fechaEntrada = moment(moment($('input[name="fechaEntrada"]').val(), 'DD-MM-YYYY')).format('YYYY-MM-DD');
                    trabajo.items.fichaTrabajo = $('input[name="fichaTrabajo"]').val();
                    trabajo.items.cliente = $('select[name="cliente"]').val();
                    trabajo.items.modelo = $('select[name="modelo"]').val();
                    trabajo.items.usuarioAsignado = $('select[name="usuarioAsignado"]').val();
                    trabajo.items.observaciones = $('input[name="observaciones"]').val();
                    trabajo.items.iva = $('input[name="iva"]').val();
                    trabajo.items.percepcion = $('input[name="percepcion"]').val();
                    trabajo.items.total = $('input[name="total"]').val();
                    trabajo.items.prioridad = $('select[name="prioridad"]').val();
                    trabajo.items.estadoTrabajo = $('select[name="estadoTrabajo"]').val();
                    var parameters = new FormData();
                    //Pasamos la accion
                    parameters.append('action', $('input[name="action"]').val());
                    //Verificamos si todos los servicios estan realizados, convertimos la accion a CONFIRM Trabajo
                    if ((estadoServicio == true) && (accion == 'edit')) {
                        var confirm = 'si';
                        parameters.append('confirm', confirm);
                    } else {
                        var confirm = 'no';
                        parameters.append('confirm', confirm);
                    }
                    //Agregamos la estructura de Trabajo con los detalles correspondientes
                    parameters.append('trabajo', JSON.stringify(trabajo.items));
                    if (accion == 'deliver') {
                        var condicion = $('select[name="selectCondicionPago"]').val();
                        parameters.append('condicionVenta', condicion);
                        var medio = $('select[name="selectMedioPago"]').val();
                        parameters.append('medioPago', medio);
                    }
                    //Bloque AJAX Trabajo
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
                                confirm_action('Notificación', '¿Desea imprimir la nota de Trabajo?', function () {
                                    window.open('/trabajos/pdf/' + data.id + '/', '_blank');
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
                },
                function () {
                    //pass
                }
            );
        }
        ;
    });
});

