#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

# declare a exchange, type is topic, named 'topic_logs'.
# topic exchange allows to do routing based on multiple criteria.
channel.exchange_declare(exchange='topic_logs',
                         type='topic')

severity = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

# a message is sent to the topic exchange with a routing_key.
# a message is identified by the routing_key.
# the topic routing_key can be like 'topic.host','topic.topic1.topic3', etc
# also can use '*'(one word) and '#'(zero or more words) to substitute word(s).
channel.basic_publish(exchange='topic_logs',
                      routing_key=severity,
                      body=message)
print " [x] Sent %r:%r" % (severity, message)
connection.close()
