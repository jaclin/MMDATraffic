
$.ajax({
    url: 'http://localhost:5000/',
    type: 'GET',
    data: {
      year: 2015,
      month: 1,
      lineID: 0,
      stationID: 25,
      bound: 0,
    }, // or $('#myform').serializeArray()
    dataType: "text",
    success: function(data) {

    var newCsv = data.split('\n').map(function(line) {
    var columns = line.split(','); // get the columns
    columns.splice(0, 1); // remove total column
    return columns
}).join('\n'); // join on newlines
      console.log(typeof(newCsv));
      draw_graph(newCsv);   
    }
});

function draw_graph(pos_data){
console.log(pos_data);
var margin = { top: 20, right: 0, bottom: 100, left: 0 },
width = 2405,
height = 255,
gridSize = 50,
legendElementWidth = gridSize * 3,
colors = ["hsl(120, 100%, 20%)", "hsl(90, 100%, 30%)", "hsl(60, 100%, 40%)", "hsl(30, 100%, 50%)", "hsl(0, 100%, 50%)"],
times = ["12:00AM", "12:30AM", "1:00AM", "1:30AM", "2:00AM", "2:30AM", "3:00AM", "3:30AM", "4:00AM", "4:30AM", "5:00AM", "5:30AM", "6:00AM", "6:30AM", "7:00AM", "7:30AM", "8:00AM", "8:30AM", "9:00AM", "9:30AM", "10:00AM", "10:30AM", "11:00AM", "11:30AM", "12:00PM", "12:30PM", "1:00PM", "1:30PM", "2:00PM", "2:30PM", "3:00PM", "3:30PM", "4:00PM", "4:30PM", "5:00PM", "5:30PM", "6:00PM", "6:30PM", "7:00PM", "7:30PM", "8:00PM", "8:30PM", "9:00PM", "9:30PM", "10:00PM", "10:30PM", "11:00PM", "11:30PM"];

data = d3.csv.parse(pos_data,
  function(d) {
    return {
      day: +d.day,
      hour: +d.hour,
      status: +d.status
    };
  });

  
    var colorScale = d3.scale.quantile().domain([0, 2])
                                        .range(colors);

    var svg = d3.select("#chart")
                .append("svg")
                .attr("width", width)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var timeLabels = svg.selectAll(".timeLabel")
                        .data(times)
                        .enter().append("text")
                        .text(function(d) { return d; })
                        .attr("x", function(d, i) { return i * gridSize; })
                        .attr("y", 0)
                        .style("text-anchor", "middle")
                        .attr("transform", "translate(" + gridSize/2 + ", -6)")
                        .attr("class", "timeLabel mono axis");

    var heatMap = svg.selectAll(".hour")
                      .data(data)
                      .enter().append("rect")
                      .attr("x", function(d) { return (d.hour/5) * gridSize; })
                      .attr("y", function(d) { return d.day * gridSize; })
                      .attr("rx", 4)
                      .attr("ry", 4)
                      .attr("class", "hour bordered")
                      .attr("width", gridSize)
                      .attr("height", gridSize)

    heatMap.transition().duration(500)
            .style("fill", function(d) { return colorScale(d.status); });

    heatMap.append("title").text(function(d) { return d.status; });
  

}