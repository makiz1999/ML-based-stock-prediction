// Global parameters:
// do not resize the chart canvas when its container does (keep at 600x400px)
Chart.defaults.global.responsive = false;
function getMetaValue(meta_name) {

    var my_arr = document.getElementsByTagName("meta");
    for (var counter = 0; counter < my_arr.length; counter++) {
        // console.log(my_arr[counter].getAttribute('property'));

        if (my_arr[counter].getAttribute('property') == meta_name) {
            return my_arr[counter].content;
        }
    }
    return "N/A";

}

function drawChart(labels, values, legend){
    //point background colors
    var colors = ["rgba(77, 175, 124, 1)", "rgba(77, 175, 124, 1)", "rgba(77, 175, 124, 1)", "rgba(77, 175, 124, 1)", "rgba(77, 175, 124, 1)", "rgba(77, 175, 124, 1)", "rgba(77, 175, 124, 1)", "rgba(77, 175, 124, 1)", "rgba(77, 175, 124, 1)", "rgba(77, 175, 124, 1)", "rgba(77, 175, 124, 1)", "rgba(77, 175, 124, 1)","rgba(77, 175, 124, 1)", "rgba(77, 175, 124, 1)", "rgba(77, 175, 124, 1)", "rgba(77, 175, 124, 1)", "rgba(77, 175, 124, 1)", "rgba(77, 175, 124, 1)", "rgba(77, 175, 124, 1)", "rgba(77, 175, 124, 1)", "rgba(255, 99, 71, 1)"];
    var colors1 = Object.assign([], colors);
    colors1.sort();

    // define the chart data
    var str = getMetaValue('labels')
    var replace= str.replace(/[\[\]]/g,'');
    var labels = replace.split(',');

    var values = JSON.parse(getMetaValue('values'))
    // console.log(values)
    var legend = getMetaValue('legend')
    // alert(legend)

    // var legend = 'UBER'
    // var labels = ['11 Oct 2021 ', '12 Oct 2021 ', '13 Oct 2021 ', '14 Oct 2021 ', '15 Oct 2021 ', '18 Oct 2021 ', '19 Oct 2021 ', '20 Oct 2021 ', '21 Oct 2021 ', '22 Oct 2021 ', '25 Oct 2021 ', '26 Oct 2021 ', '27 Oct 2021 ', '28 Oct 2021 ', '29 Oct 2021 ', '01 Nov 2021 ', '02 Nov 2021 ', '03 Nov 2021 ', '04 Nov 2021 ', '05 Nov 2021 ', 'Today']
    // var values = [46.29000091552735, 46.72000122070313, 46.40999984741212, 47.27999877929688, 48.36000061035156, 47.069999694824226, 47.049999237060554, 46.00000000000001, 46.470001220703125, 45.5099983215332, 45.720001220703125, 46.02000045776368, 44.72999954223633, 44.61999893188477, 43.81999969482422, 44.36000061035156, 42.88999938964844, 45.720001220703125, 45.27000045776367, 47.189998626708984, 46.61995580038365]
    console.log(labels)
    console.log(values)
    console.log(legend)

    var chartData = {
    labels : labels,
    datasets : [{
    label: legend,
    fill: true,
    lineTension: 0.1,
    backgroundColor: "rgba(8, 0, 197, 0.21)",
    borderColor: "rgb(60, 179, 113)",
    borderCapStyle: 'butt',
    borderDash: [],
    borderDashOffset: 0.0,
    borderJoinStyle: 'miter',
    pointBorderColor: colors,
    pointBackgroundColor: colors,
    pointBorderWidth: 4,
    pointHoverRadius: 5,
    pointHoverBackgroundColor: colors,
    pointHoverBorderColor: colors,
    pointHoverBorderWidth: 2,
    pointRadius: 1,
    pointHitRadius: 10,
    data : values,
    spanGaps: false
    }]
    }

    // get chart canvas
    var ctx = document.getElementById("myChart").getContext("2d");

    // create the chart using the chart canvas
    var myChart = new Chart(ctx, {
    type: 'line',
    data: chartData,
    });

}




