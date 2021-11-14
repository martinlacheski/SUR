var meses;
var totales;
var trabajos;
var totalesAnterior;
var trabajosAnterior;
$(document).ready(function () {
    //Realizamos el AJAX para traer las Ventas y los trabajos realizados en los ultimos 12 meses
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrftoken,
            'action': 'get_trabajos_ventas',
        },
        dataType: 'json',
        success: function (data) {
            meses = data.meses;
            totales = data.totales;
            totalesAnterior = data.totalesAnterior;
            trabajos = data.trabajos;
            trabajosAnterior = data.trabajosAnterior;
            //ARMAMOS EL GRAFICO de Evolución Anual Ventas $
            Highcharts.chart('containerVentas', {
                chart: {
                    type: 'spline'
                },
                title: {
                    text: 'Evolución Ventas - últimos 12 meses'
                },
                xAxis: {
                    categories: meses
                },
                yAxis: {
                    title: {
                        text: 'Ventas'
                    },
                    labels: {
                        formatter: function () {
                            return this.value + '$';
                        }
                    }
                },
                tooltip: {
                    crosshairs: true,
                    shared: true
                },
                plotOptions: {
                    spline: {
                        marker: {
                            radius: 4,
                            lineColor: '#666666',
                            lineWidth: 1
                        }
                    }
                },
                series: [{
                    name: 'Año Actual',
                    marker: {
                        symbol: 'square'
                    },
                    data: totales
                }, {
                    name: 'Año Anterior',
                    marker: {
                        symbol: 'diamond'
                    },
                    data: totalesAnterior
                }]
            });
            //ARMAMOS EL GRAFICO de Evolución Anual Ventas $
            Highcharts.chart('containerTrabajos', {
                chart: {
                    type: 'spline'
                },
                title: {
                    text: 'Evolución Trabajos - últimos 12 meses'
                },
                xAxis: {
                    categories: meses
                },
                yAxis: {
                    title: {
                        text: 'Trabajos'
                    },
                },
                tooltip: {
                    crosshairs: true,
                    shared: true
                },
                plotOptions: {
                    spline: {
                        marker: {
                            radius: 4,
                            lineColor: '#666666',
                            lineWidth: 1
                        }
                    }
                },
                series: [{
                    name: 'Año Actual',
                    marker: {
                        symbol: 'square'
                    },
                    data: trabajos
                }, {
                    name: 'Año Anterior',
                    marker: {
                        symbol: 'diamond'
                    },
                    data: trabajosAnterior
                }]
            });
        }
    });
});
