const routes = require('express').Router();
const playlists = require('./playlists');

routes.use('/playlists', playlists);

module.exports = routes;
