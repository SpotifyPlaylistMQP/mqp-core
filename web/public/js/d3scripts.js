/*
SECTION 1 -- Table Scripts
    All the following code is for creating the data table
*/


// builds an html string by looping through movies, adds to #results
function build_table(data, data2) { //build_table(MF, Feature MF){..}
  var html = '<table class="table-fill">'
  html = html + '<thead>'
  html = html + '<tr>'
  html = html + '<th class="text-left">K-Value</th>'
  html = html + '<th class="text-left">Matrix Factorization NDCG Score</th>'
  html = html + '<th class="text-left">Feature Matrix Factorization NDCG Score</th>'
  html = html + '</tr>'
  html = html + '</thead>'
  html = html + '<tbody class="table-hover">'
  for (var row in data) {
    if(data[row][' NDCG'] != undefined){
        var index = parseFloat(row);
        var new_row =  ''
        new_row = new_row + '<tr>'
        new_row = new_row + '<td class="text-left">'+ (index+1) +'</td>'
        new_row = new_row + '<td class="text-left">'+ Number.parseFloat(data[row][' NDCG']).toPrecision(10) +'</td>'
        new_row = new_row + '<td class="text-left">'+ Number.parseFloat(data2[row][' NDCG']).toPrecision(10) +'</td>'
        new_row = new_row + '</tr>'

        html = html + new_row;
    }
  };
  html = html + '</tbody>'
  html = html + '</table>'
  console.log(html)
  document.getElementById('result_table').innerHTML = html;
};

/*
SECTION 2 -- Legend Scripts
    All the following code is for creating the legend table
*/
// builds an html string by looping through movies, adds to #results
function build_legend() { //build_table(MF, Feature MF){..}
  var html = ''
  html = html + '<h3>Graph Legend</h3>'
  html = html + '<div> <p class="data-name"><span class="key-dot mf"></span>Matrix Factorization</p> </div>'
  html = html + '<div> <p class="data-name"><span class="key-dot feat_mf"></span>Feature Matrix Factorization</p> </div>'
  html = html + '</div>'
  document.getElementById('legendDiv').innerHTML = html;
};
