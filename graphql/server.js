var express = require('express');
var graphqlHTTP = require('express-graphql');
var {buildSchema} = require('graphql');
var amqp = require('amqplib/callback_api');

// Construct a schema, using GraphQL schema language
var schema = buildSchema(`
  type Query {
    query(ratebeer_id: Int!): [String]
  }
`);

// node sender
function sendMessage (ratebeer_id) {
  amqp.connect('amqp://rabbitmq', function(err, conn) {
    conn.createChannel(function(err, ch) {
      var q = 'node_input';
      var msg = String(ratebeer_id);

      ch.assertQueue(q, {durable: false});
      // Note: on Node 6 Buffer.from(msg) should be used
      ch.sendToQueue(q, new Buffer(msg));
      console.log(" [x] Sent %s", msg);
    });
    setTimeout(function() { conn.close(); /*process.exit(0)*/ }, 500);
  });    
}

// node receiver
function receiveMessage () {
  let isSuccess = false;

  return new Promise((resolve, reject) => {
    setTimeout(function() {
      if (!isSuccess) {
        reject('Rabbitmq timeout error');
      }
    }, 5000);

    amqp.connect('amqp://rabbitmq', function(err, conn) {
      conn.createChannel(function(err, ch) {
        var q = 'keywords';

        ch.assertQueue(q, {durable: false});
        console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", q);
        ch.consume(q, function(msg) {
          console.log(" [x] Received %s", msg.content.toString());
          resolve(JSON.parse(msg.content.toString()));
          isSuccess = true;
          conn.close();

        // return message in graphql

        }, {noAck: true});
      });
    });  
  });
}

function processGraphqlQuery(ratebeer_id) {
  sendMessage(ratebeer_id);
  return receiveMessage();
}

// The root provides a resolver function for each API endpoint
var root = {
  query: (args) => {
    // call rabbit mq here
    return processGraphqlQuery(args.ratebeer_id);
  },
};

var app = express();
app.use('/graphql', graphqlHTTP({
  schema: schema,
  rootValue: root,
  graphiql: true,
}));

// Constants
const PORT = 4000;
const HOST = '0.0.0.0';

app.listen(PORT, HOST);
console.log(`Running a GraphQL API Server at ${HOST}:${PORT}/graphql`);

// call with '{ query(ratebeer_id: XXXX)}' to localhost:4000/graphql
/* output:
{
  "data": {
    "query": [
      "guinness",
      "stout",
      "porter",
      "guiness",
      "stouts",
      "schwarzbier",
      "porters",
      "coffee",
      "oatmeal",
      "espresso"
    ]
  }
}
*/
