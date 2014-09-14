#!/usr/bin/env python
import pika

""" 1. Create a connection to a RabbitMQ server. """
connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()

""" 2. Create a queue to receive messages at the sender side.
       queue name is 'hello'
"""
#channel.queue_declare(queue='hello')

""" 3. Specify an  'exchange' and bind it with the queue.
       In RabbitMQ a message can never be sent directly to the queue, 
       it always needs to go through an 'exchange'.
       The exchange decides which queue the message should be sent to.
       The queue name is specified by 'routing_key'.
       
       In this example, a default exchange (identified by an empty string) is used.
"""
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print " [x] Sent 'Hello World!'"

""" 4. Close the connection. """
connection.close()
