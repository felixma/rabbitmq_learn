#!/usr/bin/env python
import pika

""" 1. Create a connection to a RabbitMQ server."""
connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()

""" 2. Make sure that the queue exists, 
       run the command as many times as we like, and only one will be created. 
       This step can be avoid if we're sure the queue exists.
       But we're not yet sure which program to run first. 
       In such cases it's a good practice to repeat declaring the queue 
       in both sender and receiver programs.
"""
channel.queue_declare(queue='hello')

""" 3. Define a callback function. Whenever we receive a message,
       this callback function is called by the Pika library.
"""
def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

""" 4. Subscribe the callback function to a queue. 
       We need to tell RabbitMQ that this particular callback function 
       should receive messages from our hello queue: 
"""
channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print ' [*] Waiting for messages. To exit press CTRL+C'
""" 5. Enter a never-ending loop that waits for data and runs callbacks whenever necessary."""
channel.start_consuming()
