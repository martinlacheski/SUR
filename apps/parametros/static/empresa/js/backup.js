$(function () {

    //Llamamos a la funcion de Token
    getToken(name);


    $('.btnGenerar').on('click', function () {
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'create_backup',
            },
            dataType: 'json',
            success: function (data) {
                window.open(data.url, '_blank');
            }
        });
    });
    $('.btnReestablecer').on('click', function () {
        document.getElementById('front_errors').setAttribute("hidden", "");
        let archivo = document.getElementById('id_file');
        var p_error = document.getElementById('front_errors');

        // Se comprueba si se ingresó algún archivo
        if(archivo.files.length == 0 ) {
             p_error.removeAttribute("hidden");
             p_error.innerHTML = 'No ha ingresado ningún archivo.';
        } else {
            // Se comprueba si es un .zip
            if ((archivo.value).indexOf('.zip') === -1){
                p_error.removeAttribute("hidden");
                p_error.innerHTML = 'No ha ingresado un archivo .zip';
            } else {
                $('#ajaxForm').submit();
            }
        }
    });
});

