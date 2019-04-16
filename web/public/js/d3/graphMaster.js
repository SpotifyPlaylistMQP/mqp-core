// Master Graphing Functions
// When called loads two CSV files with data and creates the D3 visualizations
// 1. Creates a table from the data ordered by K value
// 2. Creates an interactive line graph with MF and Feature MF data
var width = 400,
    height = 400;

//
var cfg = {
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
    color: d3.scaleOrdinal().range(["#F6F270", "#FF5733"])
};

//
var cfg_2 = {
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


// Queue and load the dataset (JSON/CSV) files
function d3_god(){
    //In the beginning d3_god created the CSV and the Data
    d3.queue()
        .defer(d3.csv, '/data/ndcg_values/mf_mpd_square_100.csv')
        .defer(d3.csv, '/data/ndcg_values/feature_mf_mpd_square_100.csv')
        .defer(d3.csv, '/data/ndcg_values/torch_mf_mpd_square_100.csv')
        .defer(d3.json, '/data/playlist_average.json')//play_avg
        .defer(d3.json, '/data/song_averages/song_one.json')    //song_avg
        .defer(d3.json, '/data/dataset_average.json') //data_avg
        .defer(d3.json, '/data/song_averages/song_two.json')    //song_avg
        .await(function(error, file1, file2, file3, play_avg, song_one_avg, data_avg, file6) {
            if (error) {
                console.error('Not again: ' + error);
            } else {
                bob_the_builder(file1, file2, file3, play_avg, song_one_avg, data_avg);
            };
    });
};

// Queue and run the D3 graphing functions
function bob_the_builder(file1, file2, file3, play_avg, song_one_avg, data_avg){
    d3.queue()
        //Build the line graph
        .defer(build_line_graph, file1, file2, file3)
        //Build the table
        .defer(build_table, file1, file2)
        //Build Playlist vs Dataset radar graph
        .defer(drawRadarChart, "#dataset_radar_chart", play_avg, data_avg, cfg)
        //Build Recommended Songs vs Playlist radar graph
        .defer(drawRadarChart, "#results_radar_chart", play_avg, song_one_avg, cfg_2)
        //Wait for successful completion
        .await(function(error) {
            if (error) {
                console.error('Not again #1: ' + error);
            };
        });
};
