import React, { Component } from 'react';

class SpotifyQ extends Component {
  constructor(props){
    super(props);
    this.copyAuthTokenToClipboard = this.copyAuthTokenToClipboard.bind(this);
  }

  copyAuthTokenToClipboard() {
    const el = document.createElement('textarea');
    el.value = sessionStorage.getItem('auth_token');
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
  }

  render() {
    return (
      <div className="App">
        <div className="App-header black">Spotify API App</div>
        <button className="light" onClick={this.copyAuthTokenToClipboard}>Copy Spotify Auth Token</button>
      </div>
    );
  }
}

export default SpotifyQ;
