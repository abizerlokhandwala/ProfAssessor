// This is a manifest file that'll be compiled into application.js, which will include all the files
// listed below.
//
// Any JavaScript/Coffee file within this directory, lib/assets/javascripts, or any plugin's
// vendor/assets/javascripts directory can be referenced here using a relative path.
//
// It's not advisable to add code directly here, but if you do, it'll appear at the bottom of the
// compiled file. JavaScript code in this file should be added after the last require_* statement.
//
// Read Sprockets README (https://github.com/rails/sprockets#sprockets-directives) for details
// about supported directives.
//
//= require rails-ujs
//= require turbolinks
//= require jquery3
//= require popper
//= require bootstrap
//= require d3
//= require_tree .

var pie_chart_func = function(dataset){
  $('#pie_chart').empty();
  var flag = 0;
  for(var i=0;i<dataset.length;i++){
    if(dataset[i].count>0){
      flag=1;
      break;
    }
  }
  if(flag == 0){
    $("#pie_chart").html("No Data available");
  }else{
    var width = 500
    var height = 250;

    // a circle chart needs a radius
    var radius = Math.min(width, height) / 2;

    // legend dimensions
    var legendRectSize = 15; // defines the size of the colored squares in legend
    var legendSpacing = 15; // defines spacing between squares

    // define color scale
    var color = d3.scaleOrdinal(d3.schemeCategory10);
    // more color scales: https://bl.ocks.org/pstuffa/3393ff2711a53975040077b7453781a9

    var title = d3.select('#pie_chart')
    .append('span')
    .html('STUDENT CLUSTERS')
    .style('text-align','left')
    .style('font-size','18px')
    .style('font-weight', 'bold')
    .style('line-height',1.56)
    .style('letter-spacing','1.5px')
    .style('color','rgba(0,0,0,0.64)')
    .style('padding', '10px');

    var svg = d3.select('#pie_chart') // select element in the DOM with id 'chart'
      .append('svg') // append an svg element to the element we've selected
      .attr('width', width) // set the width of the svg element we just added
      .attr('height', height) // set the height of the svg element we just added
      .append('g') // append 'g' element to the svg element
      .attr('transform', 'translate(' + (-105+width / 2) + ',' + (height / 2) + ')'); // our reference is now to the 'g' element. centerting the 'g' element to the svg element

    var arc = d3.arc()
      .innerRadius(0) // none for pie chart
      .outerRadius(radius); // size of overall chart

    var pie = d3.pie() // start and end angles of the segments
      .value(function(d) { return d.count; }) // how to extract the numerical data from each entry in our dataset
      .sort(null); // by default, data sorts in oescending value. this will mess with our animation so we set it to null

    // define tooltip_topic_wise
    var tooltip_topic_wise = d3.select('#pie_chart') // select element in the DOM with id 'chart'
      .append('div') // append a div element to the element we've selected
      .attr('class', 'tooltip_topic_wise') // add class 'tooltip_topic_wise' on the divs we just selected
      .style('width','auto');

    tooltip_topic_wise.append('div') // add divs to the tooltip_topic_wise defined above
      .attr('class', 'label') // add class 'label' on the selection
      .style('color','black');

    tooltip_topic_wise.append('div') // add divs to the tooltip_topic_wise defined above
      .attr('class', 'count'); // add class 'count' on the selection

    tooltip_topic_wise.append('div') // add divs to the tooltip_topic_wise defined above
      .attr('class', 'percent'); // add class 'percent' on the selection

    // tooltip_topic_wise.append('div') // add divs to the tooltip_topic_wise defined above
    //   .attr('class', 'difficulty'); // add class 'percent' on the selection
    // Confused? see below:

    dataset.forEach(function(d) {
      d.count = +d.count; // calculate count as we iterate through the data
      d.enabled = true; // add enabled property to track which entries are checked
    });

    // creating the chart
    var path = svg.selectAll('path') // select all path elements inside the svg. specifically the 'g' element. they don't exist yet but they will be created below
      .data(pie(dataset)) //associate dataset wit he path elements we're about to create. must pass through the pie function. it magically knows how to extract values and bakes it into the pie
      .enter() //creates placeholder nodes for each of the values
      .append('path') // replace placeholders with path elements
      .attr('d', arc) // define d attribute with arc function above
      .attr('fill', function(d) { return color(d.data.label); }) // use color scale to define fill of each label in dataset
      .each(function(d) { this._current - d; }); // creates a smooth animation for each track

    // mouse event handlers are attached to path so they need to come after its definition
    path.on('mouseover', function(d) {  // when mouse enters div
     var total = d3.sum(dataset.map(function(d) { // calculate the total number of tickets in the dataset
      return (d.enabled) ? d.count : 0; // checking to see if the entry is enabled. if it isn't, we return 0 and cause other percentages to increase
      }));
     var percent = Math.round(1000 * d.data.count / total) / 10; // calculate percent
     tooltip_topic_wise.select('.label').html(d.data.label); // set current label
     tooltip_topic_wise.select('.count').html('Number of students: '+d.data.count); // set current count
     tooltip_topic_wise.select('.percent').html("Percentage: "+percent + '%'); // set percent calculated above
     // tooltip_topic_wise.select('.difficulty').html('Very Easy: '+d.data["Very Easy"]+' Easy: ' + d.data.Easy +' Medium: ' + d.data.Medium +' Hard: ' + d.data.Hard); // set percent calculated above
     tooltip_topic_wise.style('display', 'block'); // set display
    });

    path.on('mouseout', function() { // when mouse leaves div
      tooltip_topic_wise.style('display', 'none'); // hide tooltip_topic_wise for that element
     });

    path.on('mousemove', function(d) { // when mouse moves
      tooltip_topic_wise.style('top', (d3.event.layerY + 10) + 'px') // always 10px below the cursor
        .style('left', (d3.event.layerX + 10) + 'px'); // always 10px to the right of the mouse
      });

    // define legend
    var legend = svg.selectAll('.legend') // selecting elements with class 'legend'
      .data(color.domain()) // refers to an array of labels from our dataset
      .enter() // creates placeholder
      .append('g') // replace placeholders with g elements
      .attr('class', 'legend') // each g is given a legend class
      .attr('transform', function(d, i) {
        var height = legendRectSize + legendSpacing; // height of element is the height of the colored square plus the spacing
        var offset =  height * color.domain().length / 2; // vertical offset of the entire legend = height of a single element & half the total number of elements
        var horz = 18 * legendRectSize-100; // the legend is shifted to the left to make room for the text
        var vert = i * height - offset; // the top of the element is hifted up or down from the center using the offset defiend earlier and the index of the current element 'i'
        return 'translate(' + horz + ',' + vert + ')'; //return translation
       });

    // adding colored squares to legend
    legend.append('rect') // append rectangle squares to legend
      .attr('width', legendRectSize) // width of rect size is defined above
      .attr('height', legendRectSize) // height of rect size is defined above
      .style('fill', color) // each fill is passed a color
      .style('stroke', color) // each stroke is passed a color

    // adding text to legend
    legend.append('text')
      .attr('x', legendRectSize + legendSpacing-4)
      .attr('y', legendRectSize - legendSpacing+13)
      .style('font-size','16px')
      .text(function(d) { return d; }); // return label
  }
}
