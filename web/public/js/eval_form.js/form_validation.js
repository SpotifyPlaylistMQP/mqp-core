var warning = document.getElementById('playlists_op');
    warning.onload = function () {
    warning.className = this.options[this.selectedIndex].className;
};

var op1Select = document.getElementById('op1');
    op1Select.onchange = function () {
    var op2Select = document.getElementById("playlists_op");
    var innerHTML = op2Select.options[op2Select.selectedIndex].text;
    if (innerHTML == "Select Dataset First!"){
        op2Select.remove(0)
        op2Select.disabled = false;
        op2Select.className = this.options[this.selectedIndex].className;
    }
    // populate the playlist option
    var sample = ["playlist 1", "playlist 2", "playlist 3"];
    var playlist;
    for (playlist = 0; playlist < sample.length; playlist++) {
        var x = document.getElementById("playlists_op");
        var option = document.createElement("option");
        option.text = sample[playlist];
        x.add(option);
    }
};

var playlist_select = document.getElementById('playlists_op');
    playlist_select.onchange = function () {

        var op3Select = document.getElementById("op3");
        var innerHTML = op3Select.options[op3Select.selectedIndex].text;
        if (innerHTML == "Select Playlist First!"){
            op3Select.remove(0)
            op3Select.disabled = false;
            op3Select.className = this.options[this.selectedIndex].className;
        }
};
