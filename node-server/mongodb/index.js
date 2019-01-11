const routes = require('express').Router();
const playlists = require('./playlists');
const matrices = require('./matrices');

routes.use('/playlists', playlists);
routes.use('/matrices', matrices);

module.exports = routes;
