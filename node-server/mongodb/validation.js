module.exports = {
  playlist: (playlist) => {
    const isListOfTracks = (list) => {
      let result = false;
      if (Array.isArray(list)){
        result = true;
        list.forEach(track => {
          if (track.trackId == null || typeof track.trackId !== "string" ||
              track.name == null || typeof track.name !== "string" ||
              track.artist == null || typeof track.artist !== "string"){
            result = false;
            console.log("Invalid track: ", track)
          }
        });
      }
      return result
    };

    return (
      playlist.name != null && typeof playlist.name === "string" &&
      playlist.playlistId != null && typeof playlist.playlistId === "string" &&
      playlist.tracks !== null && isListOfTracks(playlist.tracks)
    )
  }
};

{

}