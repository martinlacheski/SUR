var tablaProductos;
var tablaServicios;
//Definimos una estructura en JS para crear el PRESUPUESTO
var presupuesto = {
    items: {
        modelo: '',
        descripcion: '',
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
                {"data": "cantidad"},
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
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="Text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
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
                {"data": "cantidad"},
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
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="Text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
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

//Inicializamos a CERO los campos de importes
$(document).ready(function () {
    var accion = $('input[name="action"]').val();
    if (accion === 'add') {
        $('input[name="descripcion"]').val('');
        $('.selectMarca').val(null).trigger('change');
        $('select[name="marca"]').val(null).trigger('change');
        $('select[name="modelo"]').val(null).trigger('change');
        $('input[name="searchProductos"]').attr('disabled', true);
        $('input[name="searchServicios"]').attr('disabled', true);
    } else {
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

    //Select Anidado (Seleccionamos MARCA y cargamos los MODELOS de dicha MARCA
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

//------------------------------------MODAL MARCAS----------------------------------------//
    //Boton Marca Modal Mostrar
    $('.btnAddMarca').on('click', function () {
        $('#modalMarca').modal('show');
    });

    //Boton Marca Modal Ocultar y Resetear
    $('#modalMarca').on('hidden.bs.modal', function (e) {
        $('#formMarca').trigger('reset');
        errorList = document.getElementById("errorListMarca");
        errorList.innerHTML = '';
        location.reload();
    });

    //Submit Modal Marca
    $('#formMarca').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_marca');
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
                var newOption = new Option(data.nombre, data.id, false, true);
                $('select[name="marca"]').append(newOption).trigger('change');
                $('.selectMarca').append(newOption).trigger('change');
                $('.MarcaFormSub').append(newOption).trigger('change');
                $('#modalMarca').modal('hide');
            } else {
                var errorList = document.getElementById("errorListMarca");
                message_error(data.error, errorList);
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
        }).always(function (data) {
        });
    });

//------------------------------------MODAL MODELOS----------------------------------------//
    //Boton Modelo Modal Mostrar
    $('.btnAddModelo').on('click', function () {
        $('#modalModelo').modal('show');
    });

    //Boton Modelo Modal Ocultar y Resetear
    $('#modalModelo').on('hidden.bs.modal', function (e) {
        $('#formModelo').trigger('reset');
        errorList = document.getElementById("errorListModelo");
        errorList.innerHTML = '';
    });

    //Submit Modal Modelo
    $('#formModelo').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_modelo');
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
                var newOption = new Option(data.nombre, data.id, false, true);
                $('select[name="modelo"]').append(newOption).trigger('change');
                $('#modalModelo').modal('hide');
            } else {
                var errorList = document.getElementById("errorListModelo");
                message_error(data.error, errorList);
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
            presupuesto.addProducto(producto);
            //Una vez cargado el producto, sacamos del listado del Datatables
            tablaSearchProductos.row($(this).parents('tr')).remove().draw();
        });

//------------------------------------MODAL PRODUCTOS----------------------------------------//

    ///Boton Agregar Producto Mostrar Modal
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

//------------------------------------EVENTOS Tabla PRODUCTOS----------------------------------------//

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

//------------------------------------MODAL SERVICIOS----------------------------------------//

    ///Boton Agregar Servicio Mostrar Modal
    $('.btnAddServicio').on('click', function () {
        //Inicializamos el Codigo del Servicio
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'generar_codigo_servicio',
            },
            dataType: 'json',
            success: function (data) {
                $('.codigoServicio').val(data.codigo);
            }
        });
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

    //Al cerrar el Modal de Productos reseteamos los valores del formulario
    $('#modalServicio').on('hidden.bs.modal', function (e) {
        //Reseteamos los input del Modal
        $('#formServicio').trigger('reset');
        //Reseteamos los Select2 del Modal
        $(".ivaServicio").val('').trigger('change.select2');
        var errorList = document.getElementById("errorListFormServicio");
        errorList.innerHTML = '';
    });

    //Metodo para calcular el precio en base a los tres posibles cambios (COSTO UTILIDAD e IVA)
    $('input[name="costoServicio"]').on('change', function () {
        calcularPrecioServicio();
    });
    $('.ivaServicio').on('change', function () {
        calcularPrecioServicio();
    });

    //Funcion para calcular el precio entre COSTO UTILIDAD e IVA
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

//------------------------------------EVENTOS Tabla SERVICIOS----------------------------------------//
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
                    parameters.append('presupuestoPlantilla', JSON.stringify(presupuesto.items));
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
                                confirm_action('Notificación', '¿Desea imprimir la Plantilla de Presupuesto?', function () {
                                    window.open('/presupuestosPlantilla/pdf/' + data.id + '/', '_blank');
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

