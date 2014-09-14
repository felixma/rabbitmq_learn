#!/usr/bin/env python
import pika

# Create a connection
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

# Create a queue to receive request
channel.queue_declare(queue='rpc_queue')

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

# 'on_request' is the callback function.
# It will send a reply.
def on_request(ch, method, props, body):
    n = int(body)

    print " [.] fib(%s)"  % (n,)
    response = fib(n)

    ch.basic_publish(exchange='',
                     # send reply to 'reply_to' queue, with correlation_id
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print " [x] Awaiting RPC requests"
channel.start_consuming()
