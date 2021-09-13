$(document).ready(function() {
    var plazo = $("input[name='plazoCtaCte']").val();
    if (plazo > 0){
        document.getElementById("ctaCte").checked = true;
        $('input[name="plazoCtaCte"]').attr('disabled', false);
    }
});

$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es',
        placeholder: 'Seleccionar'
    });

    //Inicializamos los campos de tipo TOUCHSPIN
    $("input[name='limiteCtaCte']").TouchSpin({
        min: 0,
        max: 1000000,
        step: 100,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '$'
    });

    $("input[name='plazoCtaCte']").TouchSpin({
        min: 0,
        max: 1000000,
        step: 1,
        boostat: 5,
        maxboostedstep: 10,
        postfix: 'Días'
    });

    //Inicializamos error Duplicado en oculto
    $('#cuil').on('focus', function () {
            $('#ErrorDuplicado').attr("hidden", "");
        });

    $('#cuil').on('change', function () {
        $('#ErrorDuplicado').attr("hidden", "");
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
                li.innerText = value;
                errorList.appendChild(li);
            });
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

    // VALIDAMOS LOS CAMPOS
    $("#razonSocial").validate();
    $("#condicionIVA").validate();
    $("#cuil").validate();
    $("#localidad").validate();
    $("#direccion").validate();
    $("#telefono").validate();
    $("#email").validate();

    //Validamos EMAIL CORRECTO
    $("#email").on('focusout', function (e) {
        var btn = document.getElementById('btnAdd');
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
});
//agregar al campo numerico lo siguiente
//onkeypress="return isNumberKey(event)"
function isNumberKey(evt) {
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode < 48 || charCode > 57)
        return false;
    return true;
}

//Funcion para validar que el email tenga el formato correcto
function isValidEmail(mail) {
    return /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$/.test(mail);
}

