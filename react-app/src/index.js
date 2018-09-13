import React from 'react';
import ReactDOM from 'react-dom';
import registerServiceWorker from './registerServiceWorker';
import SpotifyLogin from './login/SpotifyLogin';
import AppRoot from './AppRoot';
import './AppRoot.css';
import './Styles/Colors.css'
import './Styles/Elements.css'

checkForAuthToken();

if (sessionStorage.getItem("auth_token") == null){
  ReactDOM.render(
    <SpotifyLogin />,
    document.getElementById('root')
  );
} else {
  ReactDOM.render(<AppRoot />, document.getElementById('root'));
}

registerServiceWorker();

function checkForAuthToken(){
  let hashParams = {};
  let changed = 0;
  let e, r = /([^&;=]+)=?([^&;]*)/g,
    q = window.location.hash.substring(1);
  e = r.exec(q);
  while (e) {
    hashParams[e[1]] = decodeURIComponent(e[2]);
    e = r.exec(q);
    changed++;
  }

  let auth_token, refresh_token;
  if (changed === 0){
    auth_token = null;
  } else {
    auth_token = hashParams.access_token;
    refresh_token = hashParams.refresh_token;
  }

  if (auth_token != null){
    sessionStorage.setItem("auth_token", auth_token);
    sessionStorage.setItem("refresh_token", refresh_token);
  }
}