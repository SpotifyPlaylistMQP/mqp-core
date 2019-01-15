// Builds the D3 line graph
function build_line_graph(normal_mf, feature_mf){
    // SVG variables
    var svg = d3.select('body').select('#MatrixGraph');
    var margin = {top: 40, right: 300, bottom: 40, left: 55};
    var width = +svg.attr('width') - margin.left - margin.right;
    var height = +svg.attr('height') - margin.top - margin.bottom;
    var svg = d3.select('body').select('#MatrixGraph')
        .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
        .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    // Graph variables
    var x = d3.scaleLinear().range([0, width]).nice(); //The horizontal he called X
    var y = d3.scaleLinear().range([height, 0]).nice(); //and vertical he called Y
    var formatter = d3.format('.1');
    var xAxis = d3.axisBottom().scale(x);
    var yAxis = d3.axisLeft().scale(y).tickFormat(formatter);

    // Data min and max values
    var normal_max = d3.max(normal_mf, function(d){ return d[' NDCG']; });
    var normal_min = d3.min(normal_mf, function(d){ return d[' NDCG']; });
    var feat_max = d3.max(feature_mf, function(d) { return d[' NDCG']; });
    var feat_min = d3.min(feature_mf, function(d) { return d[' NDCG']; });

    var min = Math.min(normal_min, feat_min);
    var max = Math.max(normal_max, feat_max);
    var buffer = 0.025;

    // Scale the range of the data
    x.domain(["1", "100"]);
    y.domain([min-buffer, max+buffer]);

    create_plot(normal_mf, feature_mf, svg, width, height, x, y); // Creates the elements of the graph
    add_line(normal_mf, svg, x, y, 'steelblue'); // Adds the normal MF line
    add_line(feature_mf, svg, x, y, '#FF3232'); // Adds the feture MF line
    add_legend(svg, width, normal_mf, feature_mf, x, y);
    create_overlay(normal_mf, feature_mf, svg, x, y, width, height); // Creates the interactive layover with mouse events
}

// gridlines in x axis function
function make_x_gridlines(x) {
    return d3.axisBottom(x)
        .ticks(20)
}

// gridlines in y axis function
function make_y_gridlines(y) {
    return d3.axisLeft(y)
        .ticks(20)
}

function create_plot(normal_mf, feature_mf, svg, width, height, x, y){
    // Add the X Axis
    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', 'translate(0,' + height + ')')
        .call(d3.axisBottom(x)
            .ticks(25))
        .append('text')
        .attr('x', (width/2)-5)
        .attr('y', 35)
        .attr('dx', '0.71em')
        .attr('fill', '#000')
        .attr('text-anchor', 'start')
        .style('font-weight', 'bold')
        .text('K Value');;

    // Add the Y Axis
    svg.append('g')
        .attr('class', 'axis')
        .call(d3.axisLeft(y)
            .ticks(20))
        .append('text')
        .attr('transform', 'rotate(-90)')
        .attr('x', -250)
        .attr('y', -50)
        .attr('dy', '0.71em')
        .attr('fill', '#000')
        .attr('text-anchor', 'start')
        .style('font-weight', 'bold')
        .text('NDCG Precision');

    // add the X gridlines
    svg.append("g")
        .attr("class", "line_grid")
        .attr("transform", "translate(0," + height + ")")
        .call(make_x_gridlines(x)
            .tickSize(-height)
            .tickFormat("")
        )

    // add the Y gridlines
    svg.append("g")
        .attr("class", "line_grid")
        .call(make_y_gridlines(y)
            .tickSize(-width)
            .tickFormat("")
        )
};

//Graph Functions
function add_line(data, svg, x, y, color){
    data.forEach(function(d) {
        d.n = d.n;
        d.ndcg = d.ndcg;
        d.ndcg_feat = d.ndcg_feat;
    });

    // Define the MF NDCG line
    var valueline = d3.line()
        .x(function(data) { var xval = data['N']; return x(xval); })
        .y(function(data) { var yval = data[' NDCG']; return y(yval.slice(0, 7)); });

    // Add the valueline path.
    var path = svg.append('path')
        .data([data])
        .style('fill', 'none')
        .style('stroke', color)
        .style('stroke-width', 3)
        .attr('class', 'line')
        .attr('d', valueline(data));

    var totalLength = path.node().getTotalLength();

    path
      .attr("stroke-dasharray", totalLength + " " + totalLength)
      .attr("stroke-dashoffset", totalLength)
      .transition()
        .duration(3000)
        .attr("stroke-dashoffset", 0);
};

function add_legend(svg, width, normal_mf, feature_mf, x, y){
  width = width+10;
  var mf_100 = normal_mf[99][' NDCG']; // Y Value
  var feat_100 = feature_mf[99][' NDCG']; // Y Value

  var legend = svg.append('g')
      .attr('class', 'focus')
      .style('display', 'block');

  legend.append('text')
      .attr('class', 'mf_feat_100_header')
      .attr('x', 0)
      .attr('y', 0)
      .attr('transform', 'translate(' + width + ', ' + y(feat_100) + ')')
      .style('fill', '#FF3232')
      .attr('dy', '0em')
      .text("Feature Matrix")

  legend.append('text')
      .attr('class', 'mf_feat_100_header')
      .attr('x', 0)
      .attr('y', 0)
      .attr('transform', 'translate(' + width + ', ' + y(feat_100) + ')')
      .style('fill', '#FF3232')
      .attr('dy', '1.2em')
      .text("Factorization")

  legend.append('text')
      .attr('class', 'mf_100_header')
      .attr('x', 0)
      .attr('y', 0)
      .attr('transform', 'translate(' + width + ', ' + y(mf_100) + ')')
      .style('fill', 'steelblue')
      .attr('dy', '0em')
      .text("Normal Matrix");

  legend.append('text')
      .attr('class', 'mf_100_header')
      .attr('x', 0)
      .attr('y', 0)
      .attr('transform', 'translate(' + width + ', ' + y(mf_100) + ')')
      .style('fill', 'steelblue')
      .attr('dy', '1.2em')
      .text("Factorization");
};

function create_overlay(normal_mf, feature_mf, svg, x, y, width, height){
  var focus = svg.append('g')
      .attr('class', 'focus')
      .style('display', 'none');

  focus.append('line')
      .attr('class', 'x-hover-line hover-line')
      .attr('y1', 0)
      .attr('y2', 0);

  focus.append("circle")
      .attr('class', 'red-circle')
      .attr("r", 6)
      .style("fill", "black")
      .style("stroke", '#FF3232')
      .attr('transform', 'translate(0, 100)')
      .style("stroke-width", 3)
      .style("fill-opacity", "1");

  focus.append("circle")
      .attr('class', 'blue-circle')
      .attr("r", 6)
      .style("fill", "black")
      .style("stroke", 'steelblue')
      .attr('transform', 'translate(0, 150)')
      .style("stroke-width", 3)
      .style("fill-opacity", "1");

  focus.append('text')
      .attr('class', 'mf_val')
      .attr('x', 5)
      .attr('y', 30)
      .style('fill', 'steelblue')
      .attr('dy', '.31em')
      .text(1);

  focus.append('text')
      .attr('class', 'mf_feat_val')
      .attr('x', 5)
      .attr('y', 50)
      .style('fill', '#FF3232')
      .attr('dy', '.31em')
      .text(1);

  focus.append('text')
      .attr('class', 'n_val')
      .attr('x', -15)
      .attr('y', -10)
      .attr('dy', '.31em')
      .text(1);

  var unclicked = true;
  svg.append('rect')
      .attr('transform', 'translate(0,0)')
      .attr('class', 'overlay')
      .attr('width', width)
      .attr('height', height)
      .on('mouseover', function() { focus.style('display', null); })
      .on('mouseout', function() { if(unclicked){focus.style('display', 'none'); };})
      .on('mousemove', mousemove)
      .on('click', toggle_clicked)

  function toggle_clicked(){
    unclicked = !unclicked;
    console.log(unclicked);
    if(!unclicked){
        console.log("Paused");
    };
  };

  function mousemove() {
      var x0 = Math.round(x.invert(d3.mouse(this)[0])); // Mouse X value
      var y0 = y.invert(d3.mouse(this)[0]); // Mouse Y value

      if(unclicked){
        try {
            // Matrix Factorization Y Value
            var d0 = normal_mf[x0 - 1][' NDCG']; // X-1 Y Value
            var d1 = normal_mf[x0][' NDCG']; // Y Value

            // Feature Matrix Factorization Y Value
            var c0 = feature_mf[x0 - 1][' NDCG']; // X-1 Y Value
            var c1 = feature_mf[x0][' NDCG']; // Y Value

            var d = x0 - x0 - 1 > x0 - x0 ? d1 : d0;
            var c = x0 - x0 - 1 > x0 - x0 ? c1 : c0;
        }catch(err) {};

        try {
            focus.attr('transform', 'translate(' + x(x0) + ',' + 0 + ')');

            // Text Value Display
            focus.select('.n_val').text('K: '.concat(x0));
            // focus.select('.mf_val').text('MF: '.concat(d.slice(0, 8)));
            focus.select('.mf_val').text(d.slice(0, 8));
            // focus.select('.mf_feat_val').text('Feat MF: '.concat(c.slice(0, 8)));
            focus.select('.mf_feat_val').text(c.slice(0, 8));
            focus.select('.red-circle').attr('transform', 'translate(0,' + y(c) + ')');
            focus.select('.blue-circle').attr('transform', 'translate(0,' + y(d) + ')');

            // Hover lines
            focus.select('.x-hover-line').attr('y2', height); //510 - inverse current pixel height
        }
        catch(err) {};
      };
    };
}
