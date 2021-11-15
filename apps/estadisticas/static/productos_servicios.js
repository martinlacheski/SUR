var meses;
var productos;
var servicios;
$(document).ready(function () {
    // //Inicializamos el Filtro de Rango de Fechas
    // $('input[name="filterRangoFechas"]').daterangepicker({
    //     // autoUpdateInput: false,
    //     locale: {
    //         placeholder: 'Seleccione Rango de Fechas',
    //         format: 'DD-MM-YYYY',
    //         language: 'es',
    //         cancelLabel: 'Cancelar',
    //         applyLabel: 'Aplicar',
    //     },
    //     //Remover Botones de Aplicar y Cancelar
    //     autoApply: true,
    // });
    // //Inicializamos limpio el Filtro de Rango de Fechas
    // $('input[name="filterRangoFechas"]').val('');

    //Realizamos el AJAX para traer las Ventas de Productos y Servicios en los ultimos 12 meses
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrftoken,
            'action': 'get_productos_servicios',
        },
        dataType: 'json',
        success: function (data) {
            meses = data.meses;
            productos = data.productos;
            servicios = data.servicios;
            //ARMAMOS EL GRAFICO de Evolución Anual Ventas $
            Highcharts.chart('container', {
                chart: {
                    type: 'column'
                },
                title: {
                    text: 'Venta de Productos y Servicios'
                },
                xAxis: {
                    categories: meses,
                    crosshair: true
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Pesos $'
                    }
                },
                tooltip: {
                    headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                    pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                        '<td style="padding:0"><b>{point.y:.1f} $</b></td></tr>',
                    footerFormat: '</table>',
                    shared: true,
                    useHTML: true
                },
                plotOptions: {
                    column: {
                        pointPadding: 0.2,
                        borderWidth: 0
                    }
                },
                series: [{
                    name: 'Productos',
                    data: productos
                }, {
                    name: 'Servicios',
                    data: servicios
                }]
            });
        }
    });
});