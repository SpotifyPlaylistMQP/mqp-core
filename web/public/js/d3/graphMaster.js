// Master Graphing Functions
// When called loads two CSV files with data and creates the D3 visualizations
// 1. Creates a table from the data ordered by K value
// 2. Creates an interactive line graph with MF and Feature MF data
var width = 400,
    height = 400;

// Config for the Radar chart
var config = {
    w: width,
    h: height,
    maxValue: 100,
    levels: 5,
    ExtraWidthX: 300
}

// Queue and load the dataset (JSON/CSV) files
function d3_god(){
    //In the beginning d3_god created the CSV and the Data
    d3.queue()
        .defer(d3.csv, '/data/mf_mpd_square_100')
        .defer(d3.csv, '/data/feature_mf_mpd_square_100')
        .defer(d3.json, '/data/playlist_average.json')//play_avg
        .defer(d3.json, '/data/song_averages/song_one.json')    //song_avg
        .defer(d3.json, '/data/dataset_average.json') //data_avg
        .await(function(error, file1, file2, play_avg, song_one_avg, data_avg) {
            if (error) {
                console.error('Not again: ' + error);
            } else {
                // console.log(file4)
                bob_the_builder(file1, file2, play_avg, song_one_avg, data_avg);
                // RadarChart.draw("#chart", file3, config);
            };
    });
};

// Queue and run the D3 graphing functions
function bob_the_builder(file1, file2, play_avg, song_one_avg, data_avg){
    d3.queue()
        .defer(build_line_graph, file1, file2)
        .defer(build_table, file1, file2)
        .defer(drawRadarChart_dataset, "#dataset_radar_chart", play_avg, data_avg, config)
        .defer(drawRadarChart_playlist, "#results_radar_chart", play_avg, song_one_avg, config)
        .await(function(error) {
            if (error) {
                console.error('Not again: ' + error);
            };
        });
};
