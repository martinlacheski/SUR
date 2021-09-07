$(function () {
    //Inicializamos SELECT2
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    })
    $("input[name='iva']").select2({
        postfix: '%'
    });

    //Inicializamos los campos de tipo TOUCHSPIN
    $("input[name='stockReal']").TouchSpin({
        min: 0,
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

    //Inicializamos oculto el campo de ERROR DUPLICADO
    $('#subcategoria').on('focus', function () {
        $('#ErrorDuplicado').attr("hidden", "");
    });
    //Llamamos a la funcion de Token
    getToken(name);
    //Hacemos el envio del Formulario mediante AJAX
    $("#ajaxForm").submit(function (e) {
        // VALIDACION DE LOS CAMPOS
        $("#subcategoria").validate();
        $("#descripcion").validate();
        $("#stockReal").validate();
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
                    //console.log(data.error)
                    $("#ErrorDuplicado").removeAttr("hidden");
                }
            }
        });
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

    //Boton Subcategoria Modal Mostrar
    $('.btnAddSubcategoria').on('click', function () {
        $('#modalSubcategoria').modal('show');
    });

    //Boton Subcategoria Modal Ocultar y Resetear
    $('#modalSubcategoria').on('hidden.bs.modal', function (e) {
        $('#formSubcategoria').trigger('reset');
    })

    //Boton Categoria Modal Mostrar
    $('.btnAddCategoria').on('click', function () {
        $('#modalSubcategoria').modal('hide');
        $('#modalCategoria').modal('show');
    });

    //Boton Subcategoria Modal Ocultar y Resetear
    $('#modalCategoria').on('hidden.bs.modal', function (e) {
        $('#formCategoria').trigger('reset');
    })

    //Submit Modal Subcategoría
    $('#formSubcategoria').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_subcategoria');
        parameters.append('csrfmiddlewaretoken', csrftoken);
        $.ajax({
            url: window.location.href,
            type: 'POST',
            data: parameters,
            dataType: 'json',
            processData: false,
            contentType: false,
            success: function (data) {
                if (!data.hasOwnProperty('error')) {
                    console.log(data);
                    var newOption = new Option(data.nombre, data.id, false, true);
                    $('select[name="categoria"]').append(newOption).trigger('change');
                    $('#modalSubcategoria').modal('hide');
                }
            }
        });
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
            response(data);
            console.log(data);
            if (!data.hasOwnProperty('error')) {
                //callback(data);
                console.log(data.nombre);
                console.log(data.id);
                var newOption = new Option(data.nombre, data.id, false, true);
                $('select[name="categoria"]').append(newOption).trigger('change');
                $('#modalCategoria').modal('hide');
                $('#formSubcategoria').trigger('reset');
                $('#modalSubcategoria').modal('show');
                return false;
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {

        }).always(function (data) {

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


