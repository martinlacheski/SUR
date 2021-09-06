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
    $('#id_nombre').on('focus', function () {
        $('#ErrorDuplicado').attr("hidden", "");
    });
    //Llamamos a la funcion de Token
    getToken(name);
    //Hacemos el envio del Formulario mediante AJAX
    $("#ajaxForm").submit(function (e) {
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
                    console.log(data.error)
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


