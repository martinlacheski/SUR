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

    //Inicializamos SELECT2
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    })
    $("input[name='iva']").select2({
        postfix: '%'
    });

    //Inicializamos los campos de tipo TOUCHSPIN
    $("input[name='costo']").TouchSpin({
        min: 0,
        max: 1000000,
        step: 0.1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '$'
    });

    $("input[name='esfuerzo']").TouchSpin({
        min: 1,
        max: 100,
        step: 1,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    });

    //Funcion Mostrar Errores del Formulario
    function message_error(obj) {
        var errorList = document.getElementById("errorList");
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
                    message_error(data.error);
                }
            }
        });
    });

    //Metodo para calcular el precio en base a los tres posibles cambios (COSTO UTILIDAD e IVA)
    $('input[name="costo"]').on('change', function () {
        calcularPrecio();
    });
    $('select[name="iva"]').on('change', function () {
        calcularPrecio();
    });

    // VALIDACION DE LOS CAMPOS
    $("#descripcion").validate();
    $("#costo").validate();
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
                $('input[name="precioVenta"]').val(precio.toFixed(2));
            }
        }
    });
    if (iva > 0) {
        var precio = (costo * iva);
        $('input[name="precioVenta"]').val(precio);
    }
}

$(document).ready(function () {
    var accion = $('input[name="action"]').val();
    if (accion === 'add') {
        //Inicializamos el Codigo del Servicio
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
    }
});