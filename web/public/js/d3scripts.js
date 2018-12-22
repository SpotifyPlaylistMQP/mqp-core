// builds an html string by looping through movies, adds to #results
function build_table() {
  html = ''
  html = html + '<th>K Value</th>'
  html = html + '<th>Matrix Factorization NDCG Score</th>'
  html = html + '<th>Feature Matrix Factorization NDCG Score</th>'
  document.getElementById('resultsTable').innerHTML = html;
};

function add_row(n, ndcg, ndcg_feat){
  var new_row =  ''
  new_row = new_row + '<tr>'
  new_row = new_row + '<td>'+n+'</td>'
  new_row = new_row + '<td class="ndcgtd">'+ndcg+'</td>'
  new_row = new_row + '<td class="mfndcgtd">'+ndcg_feat+'</td>'
  new_row = new_row + '</tr>'

  var html = document.getElementById('resultsTable').innerHTML;
  html = html + new_row;
  document.getElementById('resultsTable').innerHTML = html;
};
