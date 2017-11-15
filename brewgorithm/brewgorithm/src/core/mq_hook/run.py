import pika
import json
from time import sleep
from ...neural import beer2vec, beer_emb


beers_map = {}


def send_response(ratebeer_id):
  if int(ratebeer_id) not in beers_map:
    keywords = []
  else:
    beer = beers_map[int(ratebeer_id)]
    keywords = beer_emb.most_similar(positive=[beer['vector']])
    stringKeywords = [i[0] for i in keywords]

  response_connection = pika.BlockingConnection(
      pika.ConnectionParameters(host='rabbitmq', port=5672))
  response_channel = response_connection.channel()
  response_channel.queue_declare(queue='keywords')
  response_channel.basic_publish(exchange='',
                                routing_key='keywords',
                                body=json.dumps(stringKeywords))
  # above is pseudocode, need to fix
  response_connection.close()
  print(" [x] Sent", keywords)
  # above is pseudocode, need to fix


def receive_request(ch, method, properties, body):
  send_response(body)
  # sendResponse(body['params']['RatebeerID'])
  # above is pseudocode, need to fix
  print(" [x] Received %r" % body)

if __name__ == '__main__':
  beers = beer2vec.get_beer2vec()
  for beer in beers:
    beers_map[int(beer['BeerID'])] = beer
  sleep(15)
  connection = pika.BlockingConnection(
      pika.ConnectionParameters(host='rabbitmq', port=5672))
  channel = connection.channel()
  channel.queue_declare(queue='node_input')
  channel.basic_consume(receive_request,
                        queue='node_input',
                        no_ack=True)
  print(' [*] Waiting for messages. To exit press CTRL+C')
  channel.start_consuming()


# call with { query(ratebeer_id: XXXX)}

'''
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
'''
