/*
Function 1 -- Table Scripts
    All the following code is for creating the data table
*/
// builds an html string by looping through movies, adds to #results
function build_table(data, data2) { //build_table(MF, Feature MF){..}
  var html = '<table class="table-fill">'
  html = html + '<thead>'
  html = html + '<tr class="dataTable">'
  html = html + '<th class="dataTable text-left">K-Value</th>'
  html = html + '<th class="dataTable text-left">Matrix Factorization NDCG Score</th>'
  html = html + '<th class="dataTable text-left">Feature Matrix Factorization NDCG Score</th>'
  html = html + '</tr>'
  html = html + '</thead>'
  html = html + '<tbody class="table-hover">'

  for(var i = 0; i < 15; i++){
    // for (var row in data) {
        if(data[i][' NDCG'] != undefined){
            var index = i;
            var new_row =  ''
            new_row = new_row + '<tr class="dataTable">'
            new_row = new_row + '<td class="dataTable text-left">'+ (i+1) +'</td>'
            new_row = new_row + '<td class="dataTable text-left">'+ Number.parseFloat(data[i][' NDCG']).toPrecision(10) +'</td>'
            new_row = new_row + '<td class="dataTable text-left">'+ Number.parseFloat(data2[i][' NDCG']).toPrecision(10) +'</td>'
            new_row = new_row + '</tr>'
            html = html + new_row;
        // }
    }
  };
  html = html + '</tbody>'
  html = html + '</table>'
  document.getElementById('result_table').innerHTML = html;
};
