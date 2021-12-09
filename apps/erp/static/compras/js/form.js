var renglon;
var tablaProductos;
var percepcionPorcentaje = 0.00;
//Definimos una estructura en JS para crear la COMPRA
var compra = {
    items: {
        usuario: '',
        fecha: '',
        proveedor: '',
        condicionPagoCompra: '',
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
                        //return '<input type="Text" name="costoProd" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.costo + '">';
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
    var percepcion = 0.00;
    //Recorremos el Array de productos para ir actualizando los importes
    $.each(compra.items.productos, function (pos, dict) {
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
                compra.items.productos[pos].costo = parseFloat(data);
            }
        });
        dict.pos = pos;
        dict.subtotal = dict.cantidad * parseFloat(dict.costo);
        ivaCalculado += dict.subtotal * (dict.iva.iva / 100);
        subtotal += dict.subtotal;
    });
    //Asignamos los valores a los campos
    compra.items.subtotal = subtotal;
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
        $('select[name="condicionPagoCompra"]').val(null).trigger('change');
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
                //asignamos el detalle a la estructura
                compra.items.productos = data;
                //actualizamos el listado de productos
                compra.listProductos();
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

    //Validamos que no exista otro comprobante repetido del proveedor
    $("input[name='nroComprobante']").on('focusout', function () {
        var btn = document.getElementById('btnAdd');
        var proveedor = $('select[name="proveedor"]').val();
        var tipoComprobante = $('select[name="tipoComprobante"]').val();
        var nroComprobante = $('input[name="nroComprobante"]').val();
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'search_nroComprobante',
                'proveedor': proveedor,
                'tipoComprobante': tipoComprobante,
                'nroComprobante': nroComprobante,
            },
            dataType: 'json',
            success: function (data) {
                if (data.check === 'noOK') {
                    $('#errorComprobante').removeAttr("hidden");
                    btn.disabled = true;
                    $("input[name='nroComprobante']").focus();
                } else {
                    $('#errorComprobante').attr("hidden", "");
                    btn.disabled = false;
                }
            }
        });
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

    //Validamos CUIT CORRECTO
    $("#cuit").on('focusout', function (e) {
        var btn = document.getElementById('btnAddProveedor');
        if ($('input[name="cuit"]').val().lenght == 0 || !$('input[name="cuit"]').val()) {
            //cuit vacio
            $('#errorCuit').attr("hidden", "");
            btn.disabled = false;
        } else {
            var check = isValidCuit($('input[name="cuit"]').val());
            if (check == false) {
                //alert('Dirección de correo electrónico no válido');
                $("#errorCuit").removeAttr("hidden");
                btn.disabled = true;
                $("#cuit").focus();
            } else {
                $('#errorCuit').attr("hidden", "");
                btn.disabled = false;
            }
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

    $('#tablaSearchProductos tbody')
        .on('click', 'a[rel="addProducto"]', function () {
            //Asignamos a una variable el renglon que necesitamos
            var tr = tablaSearchProductos.cell($(this).closest('td, li')).index();
            //Asignamos a una variable el producto en base al renglon
            var producto = tablaSearchProductos.row(tr.row).data();
            producto.cantidad = 1;
            producto.subtotal = 0.00;
            compra.addProducto(producto);
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
                'action': 'generar_codigo',
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
        /*.on('change', 'input[name="costoProd"]', function () {
            //asignamos a una variable el costo, en la posicion actual
            var costo = parseFloat($(this).val());
            //Obtenemos la posicion del elemento a modificar dentro del Datatables
            var tr = tablaProductos.cell($(this).closest('td, li')).index();
            compra.items.productos[tr.row].costo = costo;
            //Actualizamos los importes
            calcular_importes();
            //Actualizamos el importe de subtotal en la Posicion correspondiente en cada modificación
            $('td:eq(4)', tablaProductos.row(tr.row).node()).html('$' + compra.items.productos[tr.row].subtotal.toFixed(2));
        })*/
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
                    compra.listProductos();
                    $('#modalPrecioProducto').modal('hide');

                } else {
                    message_error_precio_producto(data.error);
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
            }).always(function (data) {
            });
            //Asignamos a una variable el producto en base al renglon
            var prod = compra.items.productos[renglon];
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
        if (compra.items.productos.length === 0) {
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
                    compra.items.condicionPagoCompra = $('select[name="condicionPagoCompra"]').val();
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
    });
});