$(function () {
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


    $('.btnGenerar').on('click', function () {
        alert('btnGenerar');
    });
    $('.btnReestablecer').on('click', function () {
        // alert('btnReestablecer');
    });
});

