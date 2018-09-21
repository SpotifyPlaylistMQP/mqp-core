import React, { Component } from 'react';
import './SpotifyLogin.css';

class SpotifyLogin extends Component {
  constructor(props){
    super(props);
  }

  render() {
    return (
      <div className="spotify-login dark">
        <a href='http://localhost:8888/spotify/auth/login'>
          <img id="spotify-logo" alt="spotifyLogo" src={require('./Spotify_Logo_RGB_Green.png')}/>
        </a>
        <h1>Login to Spotify</h1>
      </div>
    );
  }

  
}

export default SpotifyLogin;
