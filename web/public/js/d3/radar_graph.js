function drawRadarChart(id, d, d2, cfg){
    // Config for the Radar chart
    var options = {
        w: width,
        h: height,
        maxValue: 100,
        levels: 5,
        ExtraWidthX: 300
    }
    if('undefined' !== typeof options){
      for(var i in options){
      if('undefined' !== typeof options[i]){
        cfg[i] = options[i];
      }
      }
    }

    cfg.maxValue = 1;

    var allAxis = (d[0].map(function(i, j){return i.area}));
    var total = allAxis.length;
    var radius = cfg.factor*Math.min(cfg.w/2, cfg.h/2);
    var Format = d3.format('.2f');
    d3.select(id).select("svg").remove();

    var g = d3.select(id)
        .append("svg")
        .attr("width", 550)
        .attr("height", cfg.h+cfg.ExtraWidthY)
        .append("g")
        .attr("transform", "translate(" + cfg.TranslateX + "," + cfg.TranslateY + ")");

		var tooltip;

    //Circular segments (Spider web lines)
    for(var j=0; j<cfg.levels; j++){
      var levelFactor = cfg.factor*radius*((j+1)/cfg.levels);
      g.selectAll(".levels")
       .data(allAxis)
       .enter()
       .append("svg:line")
       .attr("x1", function(d, i){return levelFactor*(1-cfg.factor*Math.sin(i*cfg.radians/total));})
       .attr("y1", function(d, i){return levelFactor*(1-cfg.factor*Math.cos(i*cfg.radians/total));})
       .attr("x2", function(d, i){return levelFactor*(1-cfg.factor*Math.sin((i+1)*cfg.radians/total));})
       .attr("y2", function(d, i){return levelFactor*(1-cfg.factor*Math.cos((i+1)*cfg.radians/total));})
       .attr("class", "line")
       .style("stroke", "#bec2c4")
       .style("stroke-width", "1px")
       .attr("transform", "translate(" + (cfg.w/2-levelFactor) + ", " + (cfg.h/2-levelFactor) + ")");
    }

    //Text indicating at what % each level is (on spider lines)
    for(var j=0; j<cfg.levels; j++){
      var levelFactor = cfg.factor*radius*((j+1)/cfg.levels);
      g.selectAll(".levels")
       .data([1]) //dummy data
       .enter()
       .append("svg:text")
       .attr("x", function(d){return levelFactor*(1-cfg.factor*Math.sin(0));})
       .attr("y", function(d){return levelFactor*(1-cfg.factor*Math.cos(0));})
       .attr("class", "legend")
       .style("font-family", "sans-serif")
       .style("font-size", "10px")
       .attr("transform", "translate(" + (cfg.w/2-levelFactor + cfg.ToRight) + ", " + (cfg.h/2-levelFactor) + ")")
       .attr("fill", "#000")
       .text((j+1)/cfg.levels);
    }

    series = 0;

    var axis = g.selectAll(".axis")
        .data(allAxis)
        .enter()
        .append("g")
        .attr("class", "axis");

    // Feature lines (Axis)
    axis.append("line")
      .attr("x1", cfg.w/2)
      .attr("y1", cfg.h/2)
      .attr("x2", function(d, i){return cfg.w/2*(1-cfg.factor*Math.sin(i*cfg.radians/total));})
      .attr("y2", function(d, i){return cfg.h/2*(1-cfg.factor*Math.cos(i*cfg.radians/total));})
      .attr("class", "axis");

    axis.append("text")
      .attr("class", "legend")
      .text(function(d){return d})
      .style("font-family", "sans-serif")
      .style("font-size", "11px")
      .attr("text-anchor", "middle")
      .attr('dy', '0.71em')
      .attr('fill', '#000')
      .style('font-weight', 'bold')
      .attr("transform", function(d, i){return "translate(5, -10)"})
      .attr("x", function(d, i){return cfg.w/2*(1-cfg.factorLegend*Math.sin(i*cfg.radians/total))-60*Math.sin(i*cfg.radians/total);})
      .attr("y", function(d, i){return cfg.h/2*(1-Math.cos(i*cfg.radians/total))-20*Math.cos(i*cfg.radians/total);});

    //Tooltip
    tooltip = g.append('text')
            .style('opacity', 0)
            .style('font-family', 'sans-serif')
            .style('font-size', '13px');

    //Draw the playlist average
    draw_data(d, g, cfg, total, tooltip, Format);
    draw_data(d2, g, cfg, total, tooltip, Format);
};

function redraw(song_name){
  //
  var cfg_3 = {
      radius: 5,
      w: 600,
      h: 600,
      factor: 1,
      factorLegend: .85,
      levels: 3,
      maxValue: 0,
      radians: 2 * Math.PI,
      opacityArea: 0.5,
      ToRight: 5,
      TranslateX: 80,
      TranslateY: 30,
      ExtraWidthX: 50,
      ExtraWidthY: 50,
      color: d3.scaleOrdinal().range(["#F6F270", "#25FFF0"])
  };
  // var test_name = 'song_two';
  var namecase = '/data/song_averages/'.concat(song_name).concat('.json');
  console.log(namecase);
  d3.queue()
      .defer(d3.json, namecase)
      .defer(d3.json, '/data/playlist_average.json')
      .await(function(error, file1, file2) {
          if (error) {
              console.error('Not again: ' + error);
          } else {
              drawRadarChart("#results_radar_chart", file2, file1, cfg_3);
          };
  });
};

function draw_data(d, g, cfg, total, tooltip, Format){
  d.forEach(function(y, x){
    dataValues = [];
    g.selectAll(".nodes")
    .data(y, function(j, i){
      dataValues.push([
      cfg.w/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.sin(i*cfg.radians/total)),
      cfg.h/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.cos(i*cfg.radians/total))
      ]);
    });
    dataValues.push(dataValues[0]);
    g.selectAll(".area")
           .data([dataValues])
           .enter()
           .append("polygon")
           .attr("class", "radar-chart-serie"+series)
           .style("stroke-width", "2px")
           .style("stroke", cfg.color(series))
           .attr("points",function(d) {
             var str="";
             for(var pti=0;pti<d.length;pti++){
               str=str+d[pti][0]+","+d[pti][1]+" ";
             }
             return str;
            })
           .style("fill", function(j, i){return cfg.color(series)})
           .style("fill-opacity", cfg.opacityArea)
           .on('mouseover', function (d){
                    z = "polygon."+d3.select(this).attr("class");
                    g.selectAll("polygon")
                     .transition(200)
                     .style("fill-opacity", 0.1);
                    g.selectAll(z)
                     .transition(200)
                     .style("fill-opacity", .7);
                    })
           .on('mouseout', function(){
                    g.selectAll("polygon")
                     .transition(200)
                     .style("fill-opacity", cfg.opacityArea);
           });
    series++;
  });
  series=0;


  d.forEach(function(y, x){
    g.selectAll(".nodes")
    .data(y).enter()
    .append("svg:circle")
    .attr("class", "radar-chart-serie"+series)
    .attr('r', cfg.radius)
    .attr("alt", function(j){return Math.max(j.value, 0)})
    .attr("cx", function(j, i){
        dataValues.push([
        cfg.w/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.sin(i*cfg.radians/total)),
        cfg.h/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.cos(i*cfg.radians/total))
    ]);
    return cfg.w/2*(1-(Math.max(j.value, 0)/cfg.maxValue)*cfg.factor*Math.sin(i*cfg.radians/total));
    })
    .attr("cy", function(j, i){
      return cfg.h/2*(1-(Math.max(j.value, 0)/cfg.maxValue)*cfg.factor*Math.cos(i*cfg.radians/total));
    })
    .attr("data-id", function(j){return j.area})
    .style("fill", "#fff")
    .style("stroke-width", "2px")
    .style("stroke", cfg.color(series)).style("fill-opacity", .9)
    .on('mouseover', function (d){
          newX =  parseFloat(d3.select(this).attr('cx')) - 10;
          newY =  parseFloat(d3.select(this).attr('cy')) - 10;

          tooltip
            .attr('x', newX)
            .attr('y', newY)
            .text(Format(d.value))
            .transition(200)
            .style('opacity', 1);

          z = "polygon."+d3.select(this).attr("class");
          g.selectAll("polygon")
            .transition(200)
            .style("fill-opacity", 0.1);
          g.selectAll(z)
            .transition(200)
            .style("fill-opacity", .7);
          })
    .on('mouseout', function(){
          tooltip
            .transition(200)
            .style('opacity', 0);
          g.selectAll("polygon")
            .transition(200)
            .style("fill-opacity", cfg.opacityArea);
          })
    series++;
  });
};
