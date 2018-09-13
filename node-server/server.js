let express = require('express');
let cors = require('cors');
let bodyParser = require('body-parser');

let app = express();

let SpotifyAuth = require('./SpotifyAuth');
let config = require('../config/config.json');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cors());

app.use('/spotifyAuth', SpotifyAuth);

console.log(`Listening on ${config["node-server"].port}`);
app.listen(config["node-server"].port);
