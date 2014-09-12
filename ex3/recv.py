#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

# if a exchange named 'logs' have not declared yet, then declare one, 
# or just use the existed exchange.
channel.exchange_declare(exchange='logs',
                         type='fanout')

"""
Declare a temporary queue with a random name
'exclusive=True' flag will delete the queue when the consumer dies.
"""
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

""" Bind the queue to the exchange, to tell the exchange to send messages to our queue. """
channel.queue_bind(exchange='logs',
                   queue=queue_name)

print ' [*] Waiting for logs. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] %r" % (body,)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
