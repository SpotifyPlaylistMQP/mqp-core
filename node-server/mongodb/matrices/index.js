const routes = require('express').Router();
const MongoClient = require('mongodb').MongoClient;

routes.post('/:collection', (request, response) => {
  if (request.body.matrix.length > 0){
    MongoClient.connect(process.env.MONGO_URI, {useNewUrlParser: true}, (err, db) => {
      if (err) throw err;
      const dbo = db.db('matrices');
      dbo.collection(request.params.collection).insertOne(request.body, {ordered: false}, (err, res) => {
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
    const dbo = db.db('matrices');
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

routes.delete('/:collection', (request, response) => {
  MongoClient.connect(process.env.MONGO_URI, {useNewUrlParser: true}, (err, db) => {
    if (err) throw err;
    const dbo = db.db('matrices');
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
        dbo.collection(request.params.collection).deleteMany({}, (err, obj) => {
          if (err) throw err;
          response.status(200).send()
        });
      }
    });
  });
});

console.log('POST \t/mongodb/matrices/:collection');
console.log('GET \t/mongodb/matrices/:collection');
console.log('DELETE \t/mongodb/matrices/:collection');

module.exports = routes;