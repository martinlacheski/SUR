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
        var input = document.getElementById("uploadFile");
        var fReader = new FileReader();
        fReader.readAsDataURL(input.files[0]);
        fReader.onloadend = function (event) {
            console.log(event.target.result);
            var img = document.getElementById("uploadFile");
            img.src = event.target.result;
        }
        let archivo = $('#uploadFile').val();
        // let archivo = document.getElementById("uploadFile").files[0].path
        if (archivo === '') {
            console.log('vacio');
        } else {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrftoken,
                    'action': 'restore_backup',
                    'file': archivo,
                },
                dataType: 'json',
                success: function (data) {
                    console.log(data.check);
                }
            });

        }
    });
});

