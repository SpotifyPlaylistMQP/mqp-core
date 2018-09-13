import axios from "axios";

export function getTrack(trackID){
  return axios.get('https://api.spotify.com/v1/tracks/' + trackID, {
    headers: {
      Authorization: 'Bearer ' + sessionStorage.getItem("auth_token")
    }
  });
}

export function getArtist(artistID){
  return axios.get('https://api.spotify.com/v1/artists/' + artistID, {
    headers: {
      Authorization: 'Bearer ' + sessionStorage.getItem("auth_token")
    }
  })
}

export function getAlbum(albumID) {
  return axios.get('https://api.spotify.com/v1/albums/' + albumID, {
    headers: {
      Authorization: 'Bearer ' + sessionStorage.getItem("auth_token")
    }
  });
}

export function getHistory() {
  return axios.get('https://api.spotify.com/v1/me/player/recently-played', {
    headers: {
      Authorization: 'Bearer ' + sessionStorage.getItem("auth_token")
    },
    params: {
      limit: 50,
    }
  });
}

export function getLibrary() {
  return axios.get('https://api.spotify.com/v1/me/tracks', {
    headers: {
      Authorization: 'Bearer ' + sessionStorage.getItem("auth_token")
    },
    params: {
      limit: 50,
    }
  });
}
