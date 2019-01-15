// Master Graphing Functions
// When called loads two CSV files with data and creates the D3 visualizations
// 1. Creates a table from the data ordered by K value
// 2. Creates an interactive line graph with MF and Feature MF data

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
                // After loading the data create everything
                build_table(file1, file2) // Creates the table
                build_line_graph(file1, file2); //...and earth, why not
            }
    });
};
