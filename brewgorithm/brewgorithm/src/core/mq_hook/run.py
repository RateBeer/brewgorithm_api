import pika
from time import sleep
from ...neural import beer2vec, beer_emb


beers_map = {}


def sendResponse(ratebeer_id):
  if int(ratebeer_id) not in beers_map:
    keywords = []
  else:
    beer = beers_map[int(ratebeer_id)]
    keywords = beer_emb.most_similar(positive=[beer['vector']])

  responseConnection = pika.BlockingConnection(
      pika.ConnectionParameters(host='rabbitmq', port=5672))
  responseChannel = responseConnection.channel()
  responseChannel.queue_declare(queue='keywords')
  responseChannel.basic_publish(exchange='',
                                routing_key='keywords',
                                body=keywords)
  # above is pseudocode, need to fix
  responseConnection.close()
  print(" [x] Sent", keywords)
  # above is pseudocode, need to fix


def callback(ch, method, properties, body):
  sendResponse(body['params']['RatebeerID'])
  # above is pseudocode, need to fix
  print(" [x] Received %r" % body)


if __name__ == '__main__':
  beers = beer2vec.get_beer2vec()
  for beer in beers:
    beers_map[int(beer['BeerID'])] = beer
  sleep(7)
  connection = pika.BlockingConnection(
      pika.ConnectionParameters(host='rabbitmq', port=5672))
  channel = connection.channel()
  channel.queue_declare(queue='hello')
  channel.basic_consume(callback,
                        queue='hello',
                        no_ack=True)
  print(' [*] Waiting for messages. To exit press CTRL+C')
  channel.start_consuming()


