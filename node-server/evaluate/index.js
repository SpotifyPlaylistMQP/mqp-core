const routes = require('express').Router();
const spawn = require('child_process').spawn;

routes.get('/:pid', (request, response) => {
  if (request.query.collection != null && request.query.system != null){
    const pythonProcess = spawn(
      'python',
      ["../python-code/evaluate_single_playlist.py", request.params.pid, request.query.collection, request.query.system]
    );
    pythonProcess.stdout.on('data', (data) => {
      response.status(200).send(data.toString('utf8'));
    });
  } else {
    response.status(404).send("Must call me like \"GET evaluate/{pid}?collection={mongo_collection}&system={rec-system}\"")
  }
});

console.log('GET \t/evaluate/:pid');

module.exports = routes;