#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

""" Declare a exchange, type is direct, named 'logs'. """
channel.exchange_declare(exchange='direct_logs',
                         type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

"""
a message is sent to the direct exchange with a routing_key.
a message is identified by the routing_key.
"""
channel.basic_publish(exchange='direct_logs',
                      routing_key=severity,
                      body=message)
print " [x] Sent %r:%r" % (severity, message)
connection.close()
