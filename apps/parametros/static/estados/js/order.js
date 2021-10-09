var ordenElementos;
$(function () {
    //Asignamos que los elementos sean de tipo SORTABLE
    $("#sortable").sortable({
        update: function () {
            ordenElementos = $(this).sortable("toArray");
            console.log(ordenElementos);
        }
    }).disableSelection();

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
        if (ordenElementos !== undefined) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrftoken,
                    'action': 'order',
                    'orderEstados': JSON.stringify(ordenElementos),
                },
                dataType: 'json',
                success: function (data) {
                    if (!data.hasOwnProperty('error')) {
                        location.replace(data.redirect);
                    } else {
                        message_error(data.error);
                    }
                }
            });
        } else {
            message_error('Debe modificar algún orden');
        }
    });
});