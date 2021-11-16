var modelos;
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
    //Realizamos el AJAX para traer el ranking de Modelos mas realizados en los ultimos 12 meses
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrftoken,
            'action': 'get_ranking_modelos',
        },
        dataType: 'json',
        success: function (data) {
            modelos = data;
            //ARMAMOS EL GRAFICO
            Highcharts.chart('container', {
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie'
                },
                title: {
                    text: 'Modelos más realizados - últimos 12 meses'
                },
                tooltip: {
                    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                },
                accessibility: {
                    point: {
                        valueSuffix: '%'
                    }
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                        }
                    }
                },
                series: [{
                    name: 'Porcentaje',
                    colorByPoint: true,
                    data: modelos
                }]
            });
        }
    });
});
$(function () {
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
                'action': 'get_ranking_filtrado',
                'desde': desde,
                'hasta': hasta,
            },
            dataType: 'json',
            success: function (data) {
                modelos = data;
                //ARMAMOS EL GRAFICO
                Highcharts.chart('container', {
                    chart: {
                        plotBackgroundColor: null,
                        plotBorderWidth: null,
                        plotShadow: false,
                        type: 'pie'
                    },
                    title: {
                        text: 'Modelos más realizados'
                    },
                    subtitle: {
                        text: 'Datos filtrados desde el ' + moment(desde).format('DD-MM-YYYY') + ' hasta el ' + moment(hasta).format('DD-MM-YYYY')
                    },
                    tooltip: {
                        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                    },
                    accessibility: {
                        point: {
                            valueSuffix: '%'
                        }
                    },
                    plotOptions: {
                        pie: {
                            allowPointSelect: true,
                            cursor: 'pointer',
                            dataLabels: {
                                enabled: true,
                                format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                            }
                        }
                    },
                    series: [{
                        name: 'Porcentaje',
                        colorByPoint: true,
                        data: modelos
                    }]
                });
            }
        });
    });
    //Reseteamos la pagina para limpiar el filtro
    $('input[name="filterRangoFechas"]').on('cancel.daterangepicker', function (ev, picker) {
        location.reload();
    });
});