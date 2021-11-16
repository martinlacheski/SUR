var meses;
var totales;
var trabajos;
var totalesAnterior;
var trabajosAnterior;
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
                'action': 'get_trabajos_ventas_filtradas',
                'desde': desde,
                'hasta': hasta,
            },
            dataType: 'json',
            success: function (data) {
                dias = data.dias;
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
                        text: 'Evolución Ventas'
                    },
                    subtitle: {
                        text: 'Datos filtrados desde el ' + moment(desde).format('DD-MM-YYYY') + ' hasta el ' + moment(hasta).format('DD-MM-YYYY')
                    },
                    xAxis: {
                        categories: dias
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
                        text: 'Evolución Trabajos'
                    },
                    subtitle: {
                        text: 'Datos filtrados desde el ' + moment(desde).format('DD-MM-YYYY') + ' hasta el ' + moment(hasta).format('DD-MM-YYYY')
                    },
                    xAxis: {
                        categories: dias
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
    //Reseteamos la pagina para limpiar el filtro
    $('input[name="filterRangoFechas"]').on('cancel.daterangepicker', function (ev, picker) {
        location.reload();
    });
});