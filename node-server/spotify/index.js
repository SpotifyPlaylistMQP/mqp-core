const routes = require('express').Router();
const auth = require('./auth');

routes.use('/auth', auth);

module.exports = routes;
