#!/usr/bin/env python
import sys
import pika

""" 1. Create a connection to a RabbitMQ server. """
connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()

""" 2. Create a queue to receive messages at the sender side.
       queue name is 'hello'
"""
#channel.queue_declare(queue='hello')
channel.queue_declare(queue='task_queue', durable=True)

""" 3. Specify an  'exchange' and bind it with the queue.
       In RabbitMQ a message can never be sent directly to the queue, 
       it always needs to go through an 'exchange'.
       The exchange decides which queue the message should be sent to.
       The queue name is specified by 'routing_key'.
       
       In this example, a default exchange (identified by an empty string) is used.
"""
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      #routing_key='hello',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                         ))
print " [x] Sent %r" % (message,)

""" 4. Close the connection. """
connection.close()
