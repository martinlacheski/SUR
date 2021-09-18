$(function () {
    //Inicializamos SELECT2
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    $("input[name='iva']").select2({
        postfix: '%'
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

    //Funcion Mostrar Errores del Formulario
    function message_error(obj, errorList) {
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

    //Funcion Mostrar Errores del Formulario
    function message_error_categoria(errorList) {
        errorList.innerHTML = '';
        var h5 = document.createElement("h5");
        h5.textContent = "Error:";
        errorList.appendChild(h5);
        var li = document.createElement("li");
        li.innerText = "Ya existe un/a Categoría con este/a Nombre.";
        errorList.appendChild(li);
    }

    //Llamamos a la funcion de Token
    getToken(name);

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

    //Boton Categoria Modal Mostrar
    $('.btnAddCategoria').on('click', function () {
        $('#modalCategoria').modal('show');
    });

    //Boton Categoria Modal Ocultar y Resetear
    $('#modalCategoria').on('hidden.bs.modal', function (e) {
        $('#formCategoria').trigger('reset');

        errorList = document.getElementById("errorListCategoria");
        errorList.innerHTML = '';
        location.reload();
    });


    var select_categorias = $('#CategoriaFormSub');
    //Boton Subcategoria Modal Mostrar
    $('.btnAddSubcategoria').on('click', function () {
        $('#modalSubcategoria').modal('show');
    });

    //Boton Subcategoria Modal Ocultar y Resetear
    $('#modalSubcategoria').on('hidden.bs.modal', function (e) {
        //Reseteamos los input del Modal
        $('#formSubcategoria').trigger('reset');
        //Reseteamos los Select2 del Modal
        $(".CategoriaFormSub").val('').trigger('change.select2');
        var errorList = document.getElementById("errorListSubcategoria");
        errorList.innerHTML = '';
    });

    //Submit Modal Categoría
    $('#formCategoria').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_categoria');
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
                $('#selectCategoria').append(newOption).trigger('change');
                $('#modalCategoria').modal('hide');
            } else {
                var errorList = document.getElementById("errorListCategoria");
                message_error_categoria(errorList);
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
        }).always(function (data) {
        });
    });

    //Submit Modal Subcategoría
    $('#formSubcategoria').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        console.log(parameters);
        parameters.append('action', 'create_subcategoria');
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
                $('select[name="subcategoria"]').append(newOption).trigger('change');
                $('#modalSubcategoria').modal('hide');

            } else {
                var errorList = document.getElementById("errorListSubcategoria");
                message_error(data.error, errorList);
            }
            // console.log(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {
        }).always(function (data) {
        });
    });

    //Submit Formulario Producto
    $('#ajaxForm').on('submit', function (e) {
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
        $.ajax({
            url: window.location.href,
            type: 'POST',
            data: new FormData(this),
            dataType: 'json',
            processData: false,
            contentType: false,
            success: function (data) {
                if (!data.hasOwnProperty('error')) {
                    location.replace(data.redirect);
                } else {
                    var errorList = document.getElementById("errorList");
                    message_error(data.error, errorList);
                }
            }
        });
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

});

//agregar al campo numerico lo siguiente
//onkeypress="return isNumberKey(event)"
function isNumberKey(evt) {
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode < 48 || charCode > 57)
        return false;
    return true;
}

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


