var clientes = [];
var totales = [];
var ventas = [];
var trabajos = [];
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
    //Realizamos el AJAX para traer el ranking de Clientes los ultimos 12 meses
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrftoken,
            'action': 'get_ranking_inicial',
        },
        dataType: 'json',
        success: function (data) {
            for (let i = 0; i < data.length; i++) {
                clientes.push(data[i].cliente)
                totales.push(data[i].totales)
                ventas.push(data[i].ventas)
                trabajos.push(data[i].trabajos)
            }
            //ARMAMOS EL GRAFICO
            Highcharts.chart('container', {
                chart: {
                    type: 'bar'
                },
                title: {
                    text: 'Ranking de Clientes - últimos 12 meses'
                },
                xAxis: {
                    categories: clientes,
                    title: {
                        text: null
                    }
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Pesos $',
                        align: 'high'
                    },
                    labels: {
                        overflow: 'justify'
                    }
                },
                plotOptions: {
                    bar: {
                        dataLabels: {
                            enabled: true
                        }
                    }
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'top',
                    x: -40,
                    y: -10,
                    floating: true,
                    borderWidth: 1,
                    backgroundColor:
                        Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
                    shadow: true
                },
                credits: {
                    enabled: false
                },
                series: [{
                    name: 'Total',
                    data: totales
                }, {
                    name: 'Ventas',
                    data: ventas
                }, {
                    name: 'Trabajos',
                    data: trabajos
                }]
            });
        }
    });
});
$(function () {
    //Descargamos el EXCEL de la estadistica
    $('.btnXLS').on('click', function () {
        var chart = $('#container').highcharts();
        chart.downloadXLS();
    });
    //Armamos el GRAFICO con el Filtro de FECHAS
    $('input[name="filterRangoFechas"]').on('apply.daterangepicker', function (ev, picker) {
        clientes = [];
        totales = [];
        ventas = [];
        trabajos = [];
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
                for (let i = 0; i < data.length; i++) {
                    clientes.push(data[i].cliente)
                    totales.push(data[i].totales)
                    ventas.push(data[i].ventas)
                    trabajos.push(data[i].trabajos)
                }
                //ARMAMOS EL GRAFICO
                Highcharts.chart('container', {
                    chart: {
                        type: 'bar'
                    },
                    title: {
                        text: 'Ranking de Clientes'
                    },
                    subtitle: {
                        text: 'Datos filtrados desde el ' + moment(desde).format('DD-MM-YYYY') + ' hasta el ' + moment(hasta).format('DD-MM-YYYY')
                    },
                    xAxis: {
                        categories: clientes,
                        title: {
                            text: null
                        }
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: 'Pesos $',
                            align: 'high'
                        },
                        labels: {
                            overflow: 'justify'
                        }
                    },
                    plotOptions: {
                        bar: {
                            dataLabels: {
                                enabled: true
                            }
                        }
                    },
                    legend: {
                        layout: 'vertical',
                        align: 'right',
                        verticalAlign: 'top',
                        x: -40,
                        y: -10,
                        floating: true,
                        borderWidth: 1,
                        backgroundColor:
                            Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
                        shadow: true
                    },
                    credits: {
                        enabled: false
                    },
                    series: [{
                        name: 'Total',
                        data: totales
                    }, {
                        name: 'Ventas',
                        data: ventas
                    }, {
                        name: 'Trabajos',
                        data: trabajos
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