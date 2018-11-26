const routes = require('express').Router();
const auth = require('./auth');
const audioFeatures = require('./audio-features');

routes.use('/auth', auth);
routes.use('/audio-features', audioFeatures);

module.exports = routes;
