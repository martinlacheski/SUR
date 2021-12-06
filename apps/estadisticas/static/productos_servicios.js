var meses;
var productos;
var servicios;
$(document).ready(function () {
    //Inicializamos el Filtro de Rango de Fechas
    $('input[name="filterRangoFechas"]').daterangepicker({
        // autoUpdateInput: false,
        locale: {
            placeholder: 'Seleccione Rango de Fechas',
            format: 'DD-MM-YYYY',
            language: 'es',
            cancelLabel: 'Cancelar',
            applyLabel: 'Aplicar',
        },
    });
    //Inicializamos limpio el Filtro de Rango de Fechas
    $('input[name="filterRangoFechas"]').val('');
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
                    text: 'Evolución Venta de Productos y Servicios - últimos 12 meses'
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

    //Descargamos el EXCEL de la estadistica
    $('.btnXLS').on('click', function () {
        var chart = $('#container').highcharts();
        chart.downloadXLS();
    });
    //Armamos el GRAFICO con el Filtro de FECHAS
    $('input[name="filterRangoFechas"]').on('apply.daterangepicker', function (ev, picker) {
        //Asignamos las variables Desde y Hasta
        var desde = picker.startDate.format('YYYY-MM-DD');
        var hasta = picker.endDate.format('YYYY-MM-DD');
        //Realizamos el AJAX para traer las Ventas y los trabajos realizados segun la fecha filtrada
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'action': 'get_productos_servicios_filtradas',
                'desde': desde,
                'hasta': hasta,
            },
            dataType: 'json',
            success: function (data) {
                console.log(data);
                dias = data.dias;
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
                    subtitle: {
                        text: 'Datos filtrados desde el ' + moment(desde).format('DD-MM-YYYY') + ' hasta el ' + moment(hasta).format('DD-MM-YYYY')
                    },
                    xAxis: {
                        categories: dias,
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
    //Reseteamos la pagina para limpiar el filtro
    $('input[name="filterRangoFechas"]').on('cancel.daterangepicker', function (ev, picker) {
        location.reload();
    });
    //Reseteamos la pagina para limpiar el filtrodesde el boton
    $('.btnCleanFiltros').on('click', function () {
        location.reload();
    });
});