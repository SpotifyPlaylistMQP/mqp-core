const routes = require('express').Router();
const MongoClient = require('mongodb').MongoClient;
const validation = require('../validate');

routes.post('/:collection', (request, response) => {
  // Validate the request body and if OK, set (each) playlist._id to the playlist's id
  let playlistsToInsert = [];
  if (Array.isArray(request.body)){
    request.body.forEach(playlist => {
      if (validation.playlist(playlist)){
        playlist._id = playlist.pid;
        playlistsToInsert.push(playlist)
      } else {
        response.status(400).send()
      }
    })
  } else {
    if (validation.playlist(request.body)){
      request.body._id = request.body.pid;
      playlistsToInsert.push(request.body)
    } else {
      response.status(400).send()
    }
  }

  // Insert playlistsToInsert to mongodb if there are any
  if (playlistsToInsert.length > 0){
    MongoClient.connect(process.env.MONGO_URI, {useNewUrlParser: true}, (err, db) => {
      if (err) throw err;
      const dbo = db.db('playlists');
      dbo.collection(request.params.collection).insertMany(playlistsToInsert, {ordered: false}, (err, res) => {
        response.status(204).send();
        db.close();
      });
    });
  } else {
    response.status(400).send()
  }
});

routes.get('/:collection', (request, response) => {
  MongoClient.connect(process.env.MONGO_URI, {useNewUrlParser: true}, (err, db) => {
    if (err) throw err;
    const dbo = db.db('playlists');
    dbo.listCollections().toArray((err, collections) => {
      if (err) throw err;
      let collectionParamExists = false;
      collections.forEach(collection => {
        if (collection.name === request.params.collection){
          collectionParamExists = true;
        }
      });
      if (!collectionParamExists) {
        response.status(404).send();
      } else {
        dbo.collection(request.params.collection).find({}).toArray((err, res) => {
          if (err) throw err;
          response.status(200).send(res);
          db.close();
        });
      }
    });
  });
});

console.log('POST \t/mongodb/playlists/:collection');
console.log('GET \t/mongodb/playlists/:collection');

module.exports = routes;