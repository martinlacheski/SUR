var renglon;
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
                {"data": "id"}, //Para el boton actualizar
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
                        return '<input type="Text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
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
                        return '<input type="Text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
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
    var subtotalProductos = 0.00;
    var subtotalServicios = 0.00;
    //Recorremos el Array de productos para ir actualizando los importes
    $.each(presupuesto.items.productos, function (pos, dict) {
        dict.pos = pos;
        dict.subtotal = dict.cantidad * parseFloat(dict.precioVenta);
        ivaCalculado += dict.subtotal * (dict.iva.iva / 100);
        subtotalProductos += dict.subtotal;
        subtotal += dict.subtotal;
    });
    //Recorremos el Array de servicios para ir actualizando los importes
    $.each(presupuesto.items.servicios, function (pos, dict) {
        dict.pos = pos;
        dict.subtotal = dict.cantidad * parseFloat(dict.precioVenta);
        ivaCalculado += dict.subtotal * (dict.iva.iva / 100);
        subtotalServicios += dict.subtotal;
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
    $('input[name="subtotalProductos"]').val(subtotalProductos.toFixed(2));
    $('input[name="subtotalServicios"]').val(subtotalServicios.toFixed(2));
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

$(document).ready(function () {
    //Inicializamos los Select2
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

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
    //Agregamos el Producto al Presupuesto
    $('#tablaSearchProductos tbody')
        .on('click', 'a[rel="addProducto"]', function () {
            //Asignamos a una variable el renglon que necesitamos
            var tr = tablaSearchProductos.cell($(this).closest('td, li')).index();
            //Asignamos a una variable el producto en base al renglon
            var producto = tablaSearchProductos.row(tr.row).data();
            producto.cantidad = 1;
            producto.subtotal = 0.00;
            presupuesto.addProducto(producto);
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
                    presupuesto.listProductos();
                    $('#modalPrecioProducto').modal('hide');

                } else {
                    message_error_precio_producto(data.error);
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
            }).always(function (data) {
            });
            //Asignamos a una variable el producto en base al renglon
            var prod = presupuesto.items.productos[renglon];
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
    //Agregamos el servicio al Presupuesto
    $('#tablaSearchServicios tbody')
        .on('click', 'a[rel="addServicio"]', function () {
            //Asignamos a una variable el renglon que necesitamos
            var tr = tablaSearchServicios.cell($(this).closest('td, li')).index();
            //Asignamos a una variable el servicio en base al renglon
            var servicio = tablaSearchServicios.row(tr.row).data();
            servicio.cantidad = 1;
            servicio.subtotal = 0.00;
            presupuesto.addServicio(servicio);
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
                    presupuesto.listServicios();
                    $('#modalPrecioServicio').modal('hide');

                } else {
                    message_error_precio_servicio(data.error);
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
            }).always(function (data) {
            });
            //Asignamos a una variable el Servicio en base al renglon
            var serv = presupuesto.items.servicios[renglon];
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
            if ($('input[name="action"]').val() == 'confirm') {
                $('#confirmarPresupuestoModal').modal('show');
            } else {
                confirm_action('Confirmación', '¿Estas seguro de realizar la siguiente acción?', function () {
                        // realizamos la creacion del Presupuesto mediante Ajax
                        presupuesto.items.fecha = moment(moment($('input[name="fecha"]').val(), 'DD-MM-YYYY')).format('YYYY-MM-DD');
                        presupuesto.items.validez = $('input[name="validez"]').val();
                        presupuesto.items.cliente = $('select[name="cliente"]').val();
                        presupuesto.items.modelo = $('select[name="modelo"]').val();
                        presupuesto.items.observaciones = $('input[name="observaciones"]').val();
                        var parameters = new FormData();
                        //Pasamos la accion
                        parameters.append('action', $('input[name="action"]').val());
                        //Agregamos la estructura de Presupuesto con los detalles correspondientes
                        parameters.append('presupuesto', JSON.stringify(presupuesto.items));
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
                                    confirm_action('Notificación', '¿Desea imprimir el Presupuesto?', function () {
                                        window.open('/presupuestos/pdf/' + data.id + '/', '_blank');
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
                );
            }
        }
        ;
    });
    //Submit Confirmacion de Presupuesto
    $('#confirmarPresupuestoModal').on('submit', function (e) {
        e.preventDefault();
        if (presupuesto.items.productos.length === 0 && presupuesto.items.servicios.length === 0) {
            error_action('Error', 'Debe al menos tener un producto o servicio en sus detalles', function () {
                //pass
            }, function () {
                //pass
            });
        } else {
            // realizamos la creacion del Presupuesto mediante Ajax
            presupuesto.items.fecha = moment(moment($('input[name="fecha"]').val(), 'DD-MM-YYYY')).format('YYYY-MM-DD');
            presupuesto.items.validez = $('input[name="validez"]').val();
            presupuesto.items.cliente = $('select[name="cliente"]').val();
            presupuesto.items.modelo = $('select[name="modelo"]').val();
            presupuesto.items.observaciones = $('input[name="observaciones"]').val();
            var parameters = new FormData();
            //Pasamos la accion
            parameters.append('action', $('input[name="action"]').val());
            //Pasamos la prioridad del Trabajo
            parameters.append('prioridad', $('select[name="selectPrioridad"]').val());
            //parameters.append('csrfmiddlewaretoken', csrftoken);
            //Agregamos la estructura de Presupuesto con los detalles correspondientes
            parameters.append('presupuesto', JSON.stringify(presupuesto.items));
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
                        confirm_action('Notificación', '¿Desea imprimir el Presupuesto?', function () {
                            window.open('/presupuestos/pdf/' + data.id + '/', '_blank');
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
    });
});

