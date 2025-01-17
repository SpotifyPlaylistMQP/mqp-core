const server = require('express')();
const bodyParser = require('body-parser');

require('dotenv').load();

server.use(require('cors')());
server.use(bodyParser({limit: '50mb'}));
server.use(bodyParser.json());
server.use(bodyParser.urlencoded({ extended: true }));

server.use(require('./logRequests'));

server.use('/spotify', require('./spotify'));
server.use('/mongodb', require('./mongodb'));
server.use('/evaluate', require('./evaluate'));

server.listen(process.env.PORT, () => {
  console.log(`Server listening on port ${process.env.PORT}`);
});
