import pika
from time import sleep
from ...neural import beer2vec


def sendResponse(beers_map, ratebeer_id):
  beer = beers_map[ratebeer_id]

  responseConnection = pika.BlockingConnection(
      pika.ConnectionParameters(host='rabbitmq', port=5672))
  responseChannel = responseConnection.channel()
  responseChannel.queue_declare(queue='keywords')
  responseChannel.basic_publish(exchange='',
                                routing_key='keywords',
                                body=beer['keywords'])
  # above is pseudocode, need to fix
  responseConnection.close()
  print(" [x] Sent", beer['keywords'])
  # above is pseudocode, need to fix


def create_callback():
  beers = beer2vec.get_beer2vec()
  beers_map = {}
  for beer in beers:
    beers_map[beer['RatebeerID']] = beer
  def callback(ch, method, properties, body):
    sendResponse(beers_map, body['params']['RatebeerID'])
    # above is pseudocode, need to fix
    print(" [x] Received %r" % body)
  return callback

if __name__ == '__main__':
  sleep(7)
  connection = pika.BlockingConnection(
      pika.ConnectionParameters(host='rabbitmq', port=5672))
  channel = connection.channel()
  channel.queue_declare(queue='hello')
  channel.basic_consume(create_callback(),
                        queue='hello',
                        no_ack=True)
  print(' [*] Waiting for messages. To exit press CTRL+C')
  channel.start_consuming()


