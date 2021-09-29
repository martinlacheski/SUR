  $(function () {

    var tipoVentasMes = {
      labels  : ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
      datasets: [
        {
          label               : 'Productos',
          backgroundColor     : 'rgba(60,141,188,0.9)',
          borderColor         : 'rgba(60,141,188,0.8)',
          pointRadius          : false,
          pointColor          : '#3b8bba',
          pointStrokeColor    : 'rgba(60,141,188,1)',
          pointHighlightFill  : '#fff',
          pointHighlightStroke: 'rgba(60,141,188,1)',
          data                : [95, 75, 62, 49, 46, 42, 65, 68, 70, 65, 80, 85]
        },
        {
          label               : 'Servicios',
          backgroundColor     : 'rgba(210, 214, 222, 1)',
          borderColor         : 'rgba(210, 214, 222, 1)',
          pointRadius         : false,
          pointColor          : 'rgba(210, 214, 222, 1)',
          pointStrokeColor    : '#c1c7d1',
          pointHighlightFill  : '#fff',
          pointHighlightStroke: 'rgba(220,220,220,1)',
          data                : [70, 50, 45, 35, 32, 35, 55, 52, 45, 59, 69, 78]
        },
      ]
    }

    var trabajosPorMes = {
      labels  : ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
      datasets: [
        {
          label               : 'Año actual',
          backgroundColor     : 'rgba(60,141,188,0.9)',
          borderColor         : 'rgba(60,141,188,0.8)',
          pointRadius          : false,
          pointColor          : '#3b8bba',
          pointStrokeColor    : 'rgba(60,141,188,1)',
          pointHighlightFill  : '#fff',
          pointHighlightStroke: 'rgba(60,141,188,1)',
          data                : [95, 75, 62, 49, 46, 37, 65, 68, 70, 65, 80, 85]
        },
        {
          label               : 'Año Anterior',
          backgroundColor     : 'rgba(210, 214, 222, 1)',
          borderColor         : 'rgba(210, 214, 222, 1)',
          pointRadius         : false,
          pointColor          : 'rgba(210, 214, 222, 1)',
          pointStrokeColor    : '#c1c7d1',
          pointHighlightFill  : '#fff',
          pointHighlightStroke: 'rgba(220,220,220,1)',
          data                : [90, 70, 62, 45, 43, 42, 63, 70, 68, 59, 75, 82]
        },
      ]
    }

    var areaChartOptions = {
      maintainAspectRatio : false,
      responsive : true,
      legend: {
        display: true
      },
      scales: {
        xAxes: [{
          gridLines : {
            display : false,
          }
        }],
        yAxes: [{
          gridLines : {
            display : false,
          }
        }]
      }
    }

    //-------------
    //- Ventas por mes
    //-------------

    var barChartCanvas = $('#barChart').get(0).getContext('2d')
    var barChartData = $.extend(true, {}, tipoVentasMes)
    var temp0 = tipoVentasMes.datasets[0]
    var temp1 = tipoVentasMes.datasets[1]
    barChartData.datasets[0] = temp0
    barChartData.datasets[1] = temp1

    var barChartOptions = {
      responsive              : true,
      maintainAspectRatio     : false,
      datasetFill             : false
    }
    //Creamos el Grafico
    new Chart(barChartCanvas, {
      type: 'bar',
      data: barChartData,
      options: barChartOptions
    })

    //-------------
    //- Cantidad de Tapas de Cilindro por mes
    //--------------
    var lineChartCanvas = $('#lineChart').get(0).getContext('2d')
    var lineChartOptions = $.extend(true, {}, trabajosPorMes)
    var lineChartData = $.extend(true, {}, trabajosPorMes)
    lineChartData.datasets[0].fill = false;
    lineChartData.datasets[1].fill = false;
    lineChartOptions.datasetFill = false

    //Creamos el Grafico
    var lineChart = new Chart(lineChartCanvas, {
      type: 'line',
      data: lineChartData,
      options: lineChartOptions
    })

    //-------------
    //- Ranking de tapas de cilindro por mes
    //-------------

    var pieChartCanvas = $('#pieChart').get(0).getContext('2d')
    var donutData        = {
      labels: [
          'Tapa 1',
          'Tapa 2',
          'Tapa 3',
          'Tapa 4',
          'Tapa 5',
          'Tapa 6',
          'Tapa 7',
          'Tapa 8',
          'Tapa 9',
          'Tapa 10',
      ],
      datasets: [
        {
          data: [20,15,10,8,12,8,3, 4, 5, 2],
          backgroundColor : ['#f56954', '#00a65a', '#f39c12', '#00c0ef', '#3c8dbc', '#d2d6de', '#00009c', '#871f78', '#8f8fbd', '#db70db', '#d2d6de', '#d2d6de' ],
        }
      ]
    }
    var pieData        = donutData;
    var pieOptions     = {
      maintainAspectRatio : false,
      responsive : true,
    }
    //Creamos el grafico
    new Chart(pieChartCanvas, {
      type: 'pie',
      data: pieData,
      options: pieOptions
    })

    //-------------
    //- Ranking de Clientes por mes
    //-------------

    var donutChartCanvas = $('#donutChart').get(0).getContext('2d')
    var donutData        = {
      labels: [
          'Cliente 1',
          'Cliente 2',
          'Cliente 3',
          'Cliente 4',
          'Cliente 5',
          'Cliente 6',
          'Cliente 7',
          'Cliente 8',
          'Cliente 9',
          'Cliente 10',
      ],
      datasets: [
        {
          data: [20,15,10,5,10,5,10, 8, 12, 15],
          backgroundColor : ['#f56954', '#00a65a', '#f39c12', '#00c0ef', '#3c8dbc', '#d2d6de', '#00009c', '#871f78', '#8f8fbd', '#db70db', '#d2d6de', '#d2d6de' ],
        }
      ]
    }
    var donutOptions     = {
      maintainAspectRatio : false,
      responsive : true,
    }
    //Creamos el Grafico
    new Chart(donutChartCanvas, {
      type: 'doughnut',
      data: donutData,
      options: donutOptions
    })
  })
