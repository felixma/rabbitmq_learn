#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

"""
Declare a exchange, type is fanout(means broadcast),named 'logs'.
Exchange is used to receive messages form producer, and send messages to queue.
There are four exchange types: direct, topic, headers and fanout
"""
channel.exchange_declare(exchange='logs',
                         type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs',
                      routing_key='', #routing_key is '', because 'fanout' exchange will ignore its value.
                      body=message)
print " [x] Sent %r" % (message,)
connection.close()
