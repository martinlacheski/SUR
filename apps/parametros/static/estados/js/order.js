$(function () {
    $("#sortable").sortable({
        update: function () {
            var ordenElementos = $(this).sortable("toArray");
            for (order in ordenElementos) {
                console.log(order.id);
            }
        }
    }).disableSelection();
});