// Master Graphing Functions
// When called loads two CSV files with data and creates the D3 visualizations
// 1. Creates a table from the data ordered by K value
// 2. Creates an interactive line graph with MF and Feature MF data
var width = 300,
    height = 300;

// Config for the Radar chart
var config = {
    w: width,
    h: height,
    maxValue: 100,
    levels: 5,
    ExtraWidthX: 300
}

function d3_god(){
    //In the beginning d3_god created the CSV and the Data
    d3.queue()
        .defer(d3.csv, '/data/mf_mpd_square_100')
        .defer(d3.csv, '/data/feature_mf_mpd_square_100')
        .defer(d3.json, '/data/data.json')
        .await(function(error, file1, file2, file3) {
            if (error) {
                console.error('Not again: ' + error);
            } else {
                console.log(file3)
                bob_the_builder(file1, file2);
                RadarChart.draw("#chart", file3, config);
            };
    });
};

function bob_the_builder(file1, file2){
    d3.queue()
        .defer(build_line_graph, file1, file2)
        .defer(build_table, file1, file2)
        .await(function(error) {
            if (error) {
                console.error('Not again: ' + error);
            };
        });
};
