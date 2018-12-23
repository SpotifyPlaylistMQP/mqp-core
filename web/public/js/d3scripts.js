function d3_god(){
    //In the beginning d3_god created the CSV and the Data
    d3.queue()
        .defer(d3.csv, '/data/mf_mpd_square_100')
        .defer(d3.csv, '/data/feature_mf_mpd_square_100')
        .await(function(error, file1, file2) {
            if (error) {
                console.error('Not again: ' + error);
            }
            else {
                earth(file1, file2); //...and earth, why not
            }
    });
};

function earth(file1, file2){
    //And d3_god said, "let there be SVG dimensions," and there was SVG dimensions
    var svg = d3.select('svg');

    // d3_god saw that the SVG dimensions were good, and seperated the dimensions
    var margin = {top: 50, right: 20, bottom: 40, left: 50},
        width = +svg.attr('width') - margin.left - margin.right,
        height = +svg.attr('height') - margin.top - margin.bottom;

    // Thus d3_god said, "Let there be a dimension between the dimensions to seperate the X from the Y"
    var x = d3.scaleLinear().range([0, width]).nice(); //The horizontal he called X
    var y = d3.scaleLinear().range([height, 0]).nice(); //and vertical he called Y

    //"Let the table under the graph be gathered in one place"
    var svg = d3.select('body').select('#MatrixGraph')
        .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
        .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    //Then d3_god said, "The table produce values: K values and accurate NDCG bearing results", and it was so
    build_table(file1, file2) //Creates the table
    step_one(file1, file2, x, y, margin, width, height, svg); //Creates all the D3 Graph stuff
}

// builds an html string by looping through movies, adds to #results
function build_table(data, data2) { //build_table(MF, Feature MF){..}
  html = ''
  html = html + '<th>K Value</th>'
  html = html + '<th>Matrix Factorization NDCG Score</th>'
  html = html + '<th>Feature Matrix Factorization NDCG Score</th>'
  document.getElementById('resultsTable').innerHTML = html;

  var d = '';
  for (var row in data) {
    if(data[row][' NDCG'] != undefined){
        var index = parseFloat(row);
        var new_row =  ''
        new_row = new_row + '<tr>'
        new_row = new_row + '<td>'+ (index+1) +'</td>'
        new_row = new_row + '<td class="ndcgtd">'+ data[row][' NDCG'] +'</td>'
        new_row = new_row + '<td class="mfndcgtd">'+ data2[row][' NDCG'] +'</td>'
        new_row = new_row + '</tr>'

        var html = document.getElementById('resultsTable').innerHTML;
        html = html + new_row;
        document.getElementById('resultsTable').innerHTML = html;
    }
  };
};

function step_one(normal_mf, feature_mf, x, y, margin, width, height, svg){
    var formatter = d3.format('.1');
    var xAxis = d3.axisBottom().scale(x);
    var yAxis = d3.axisLeft().scale(y).tickFormat(formatter);

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

    create_graph(normal_mf, feature_mf, svg, width, height, x, y); // Creates the elements of the graph
    add_normal_line(normal_mf, svg, x, y); // Adds the normal MF line
    add_feature_line(feature_mf, svg, x, y); // Adds the feture MF line
    create_overlay(normal_mf, feature_mf, svg, x, y, width, height); // Creates the interactive layover with mouse events
};

function create_graph(normal_mf, feature_mf, svg, width, height, x, y){
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
};

//Graph Functions
function add_normal_line(data, svg, x, y){
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
    svg.append('path')
        .data([data])
        .style('fill', 'none')
        .style('stroke', 'steelblue')
        .style('stroke-width', 3)
        .attr('class', 'line')
        .attr('d', valueline(data));
};

function add_feature_line(data, svg, x, y){
    data.forEach(function(d) {
        d.n = d.n;
        d.ndcg = d.ndcg;
        d.ndcg_feat = d.ndcg_feat;
    });

    // Define the Feature MF NDCG line
    var valueline = d3.line()
        .x(function(data) { var xval = data['N']; return x(xval); })
        .y(function(data) { var yval = data[' NDCG']; return y(yval.slice(0, 7)); });

    svg.append('path')
        .data(data)
        .style('fill', 'none')
        .style('stroke', '#FF3232')
        .style('stroke-width', 3)
        .attr('class', 'line')
        .attr('d', valueline(data));
};

function create_overlay(normal_mf, feature_mf, svg, x, y, width, height){
  var focus = svg.append('g')
      .attr('class', 'focus')
      .style('display', 'none');

  focus.append('line')
      .attr('class', 'x-hover-line hover-line')
      .attr('y1', 0)
      .attr('y2', 0);

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

  svg.append('rect')
      .attr('transform', 'translate(0,0)')
      .attr('class', 'overlay')
      .attr('width', width)
      .attr('height', height)
      .on('mouseover', function() { focus.style('display', null); })
      .on('mouseout', function() { focus.style('display', 'none'); })
      .on('mousemove', mousemove);

  function mousemove() {
      var x0 = Math.round(x.invert(d3.mouse(this)[0])); // Mouse X value
      var y0 = y.invert(d3.mouse(this)[0]); // Mouse Y value

      // Matrix Factorization Y Value
      var d0 = normal_mf[x0 - 1][' NDCG']; // X-1 Y Value
      var d1 = normal_mf[x0][' NDCG']; // Y Value

      // Feature Matrix Factorization Y Value
      var c0 = feature_mf[x0 - 1][' NDCG']; // X-1 Y Value
      var c1 = feature_mf[x0][' NDCG']; // Y Value

      var d = x0 - x0 - 1 > x0 - x0 ? d1 : d0;
      var c = x0 - x0 - 1 > x0 - x0 ? c1 : c0;
      focus.attr('transform', 'translate(' + x(x0) + ',' + 0 + ')');

      // Text Value Display
      focus.select('.n_val').text('K: '.concat(x0));
      focus.select('.mf_val').text('MF: '.concat(d.slice(0, 7)));
      focus.select('.mf_feat_val').text('Feat MF: '.concat(c.slice(0, 7)));

      // Hover lines
      focus.select('.x-hover-line').attr('y2', height); //510 - inverse current pixel height
    }
}
