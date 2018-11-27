module.exports = {
  playlist: (playlist) => {
    const isListOfTracks = (list) => {
      let result = false;
      if (Array.isArray(list)){
        result = true;
        list.forEach(track => {
          if (track.tid == null || typeof track.tid !== "string" ||
              track.name == null || typeof track.name !== "string" ||
              track.artist == null || typeof track.artist !== "string" ||
              track.danceability == null || typeof track.danceability !== "number" ||
              track.energy == null || typeof track.energy !== "number" ||
              track.tempo == null || typeof track.tempo !== "number" ||
              track.valence == null || typeof track.valence !== "number"){
            result = false;
            console.log("Invalid track: ", track)
          }
        });
      }
      return result
    };

    return (
      playlist.name != null && typeof playlist.name === "string" &&
      playlist.pid != null && typeof playlist.pid === "string" &&
      playlist.tracks !== null && isListOfTracks(playlist.tracks)
    )
  }
};