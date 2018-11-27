const routes = require('express').Router();
const request = require('request');

routes.get('/', function(req, res) {
  if (req.query.tids.split(',').length > 100){
    res.send({error: 'Cannot send over 100 Track IDs'})
  }
  const requestOptions = {
    url: `https://api.spotify.com/v1/audio-features?ids=${req.query.tids}`,
    headers: {
      Authorization: 'Bearer ' + global.authToken
    }
  };
  request.get(requestOptions, function(error, response, body) {
    if (!error && response.statusCode === 200) {
      res.send(body)
    } else {
      console.log(response.statusCode);
      console.log(error);
      res.send({error: 'Cannot connect to the Spotify API'})
    }
  });
});

console.log('GET \t/spotify/audio-features');

module.exports = routes;