(function (Highcharts) {
  var each = Highcharts.each;
  Highcharts.wrap(Highcharts.Legend.prototype, 'renderItem', function (proceed, item) {
      proceed.call(this, item);
      var series = this.chart.series, element = item.legendGroup.element;
      element.onmouseover = function () {
         each(series, function (seriesItem) {
              if (seriesItem !== item) {
                  each(['group', 'markerGroup'], function (group) {
                      seriesItem[group].attr('opacity', 0.25);
                  });
              }
          });
      }
      element.onmouseout = function () {
         each(series, function (seriesItem) {
              if (seriesItem !== item) {
                  each(['group', 'markerGroup'], function (group) {
                      seriesItem[group].attr('opacity', 1);
                  });
              }
          });
      }
  });
}(Highcharts));

// The "detail chart" is the larger, top chart.  The "master chart" is the one
// on bottom, where you can select a date range.
function createDetail(masterChart) {
    // create a detail chart referenced by a global variable
    detailChart = $('#detail-container').highcharts({
        chart: {
            marginBottom: 120,
            marginTop: 50,
            reflow: false,
            marginLeft: 50,
            marginRight: 20,
            style: { position: 'absolute' }
        },
        credits: { enabled: false },
        title: { text: null },
        xAxis: {
            type: 'datetime',
            min: yesterday,
            max: now
        },
        yAxis: {
            title: { text: null },
            maxZoom: 0.1,
            min: 0,
            max: 10
        },
        tooltip: {
            formatter: function() {
                var point = this.points[0];
                return '<b>'+ point.series.name +':</b> ' + point.point.name + '<br/>' +
                    Highcharts.dateFormat('%A %B %e %Y', this.x) + ':<br/>'+
                    Highcharts.dateFormat('%I:%M:%S %p', this.x);
            },
            shared: true
        },
        legend: {
          enabled: true,
          floating: true,
          verticalAlign: "top",
          margin: 50
        },
        plotOptions: {
            series: {
                marker: {
                    enabled: false,
                    states: {
                        hover: {
                            enabled: true,
                            radius: 3
                        }
                    }
                }
            }
        },
        series: series,
    }).highcharts(); // return chart
}

// listen to the selection event on the master chart to update the
// extremes of the detail chart
function selection(event) {
  var extremes = event.xAxis[0];
  var xAxis = this.xAxis[0];

  // move the plot bands to reflect the new detail span
  xAxis.removePlotBand('mask-before');
  xAxis.addPlotBand({
      id: 'mask-before',
      from: earliestDate,
      to: extremes.min,
      color: 'rgba(0, 0, 0, 0.2)'
  });

  xAxis.removePlotBand('mask-after');
  xAxis.addPlotBand({
      id: 'mask-after',
      from: extremes.max,
      to: latestDate,
      color: 'rgba(0, 0, 0, 0.2)'
  });
  detailChart.xAxis[0].setExtremes(extremes.min, extremes.max);
  return false;
}

function createMaster() {
  masterChart = $('#master-container').highcharts({
      chart: {
          reflow: false,
          borderWidth: 0,
          backgroundColor: null,
          marginLeft: 50,
          marginRight: 20,
          zoomType: 'x',
          events: { selection: selection }
      },
      title: { text: null },
      xAxis: {
          type: 'datetime',
          showLastTickLabel: true,
          maxZoom: dayMillis, // one day
          max: now,
          plotBands: [{
              id: 'mask-before',
              from: earliestDate,
              to: yesterday,
              color: 'rgba(0, 0, 0, 0.2)'
          }],
          title: { text: null }
      },
      yAxis: {
          gridLineWidth: 0,
          labels: { enabled: false },
          title: { text: null },
          showFirstLabel: false,
          min: 0,
          max: 10
      },
      tooltip: { formatter: function() { return false; } },
      legend: { enabled: false },
      credits: { enabled: false },
      plotOptions: {
          series: {
              fillColor: {
                  linearGradient: [0, 0, 0, 70],
                  stops: [
                      [0, '#4572A7'],
                      [1, 'rgba(0,0,0,0)']
                  ]
              },
              lineWidth: 1,
              marker: { enabled: false },
              shadow: false,
              states: { hover: { lineWidth: 1 } },
              enableMouseTracking: false
          }
      },
      series: series,

  }, function(masterChart) { createDetail(masterChart) })
  .highcharts(); // return chart instance
}

$(document).ready(function() {
  // make the container smaller and add a second container for the master chart
  var $container = $('#container')
      .css('position', 'relative');

  var $detailContainer = $('<div id="detail-container">')
      .appendTo($container);

  var $masterContainer = $('<div id="master-container">')
      .css({ position: 'absolute', top: 300, height: 80, width: '100%' })
      .appendTo($container);

  // create master and in its callback, create the detail chart
  createMaster();
});
