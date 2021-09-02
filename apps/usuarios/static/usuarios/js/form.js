$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es',
        placeholder: 'Seleccionar'
    });
    <!-- Inicialización de datetimepicker -->
    $('#fechaIngreso').datetimepicker({
        format: 'DD/MM/yyyy',
        locale: 'es',
        icons: {date: 'far fa-calendar-alt'},
    });
    //Llamamos a la funcion de Token
    $('#id_nombre').on('focus', function () {
        $('#ErrorDuplicado').attr("hidden", "");
    });
    getToken(name);
    $("#ajaxForm").submit(function (e) {
        e.preventDefault();
        $.ajax({
            url: window.location.href,
            type: 'POST',
            // data: $(this).serialize(),
            // Reemplazamos DATA por lo siguiente para que se pueda enviar los datos de tipo FILES
            data: new FormData(this),
            // Agregamos los siguientes valores para poder enviar por AJAX datos de tipo FILES
            dataType: 'json',
            processData: false,
            contentType: false,
            success: function (data) {
                if (data.check === 'Registrar') {
                    //Lo registramos. Nos vamos a otro lado
                    location.replace(data.redirect);
                } else if (data.check === true) {
                    // Mostramos el error
                    $("#ErrorDuplicado").removeAttr("hidden");
                } else {
                    // no hacemos nada. Pero nos vamos a otro lado tmb
                    location.replace(data.redirect);
                }
            }
        });
    });

    // VALIDAMOS LOS CAMPOS
    $("#username").validate();
    $("#password").validate();
    $("#first_name").validate();
    $("#last_name").validate();
    $("#cuil").validate();
    $("#email").validate();
    $("#legajo").validate();
    $("#fechaIngreso").validate();
    $("#localidad").validate();
    $("#direccion").validate();

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

