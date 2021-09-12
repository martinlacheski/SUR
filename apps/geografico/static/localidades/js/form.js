$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    //Select Anidado (Seleccionamos PAIS y cargamos las PROVINCIAS de dicho PAIS
    var select_provincias = $('select[name="provincia"]');
    $('select[name="pais"]').on('change', function () {
        var id = $(this).val();
        var options = '<option value="">---------</option>';
        if (id === '') {
            select_provincias.html(options);
            return false;
        }
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'search_provincias',
                'pk': id
            },
            dataType: 'json',
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                //Volvemos a cargar los datos del Select2 solo que los datos (data) ingresados vienen por AJAX
                select_provincias.html('').select2({
                    theme: "bootstrap4",
                    language: 'es',
                    data: data
                });
                return false;
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
        }).always(function (data) {
        });
    });
});