# import pika
# #参考https://www.jianshu.com/p/76875d2381c0
#
# config = pika.ConnectionParameters(
#     host='127.0.0.1',
#     port=5672,
#     credentials=pika.PlainCredentials('test', 'test'),
# )
#
# conn = pika.BlockingConnection(config)
# channel = conn.channel()
#
# channel.exchange_declare(exchange='ceshi', exchange_type='direct')
#
# channel.queue_declare(queue='hello')
#
# channel.queue_bind(exchange='ceshi', queue='hello', routing_key='1')
#
# def callback(channel, method, properties, body):
#     print(channel)
#     print(method)
#     print(properties)
#     print(body)
#
# channel.basic_consume(
#     callback,
#     queue='hello',
#     no_ack=False
# )
# print('waiting...')
# channel.start_consuming()

import pika
import sys
import time

# 远程rabbitmq服务的配置信息
username = 'admin'
pwd = 'admin'
# ip_addr = '10.1.7.7'
ip_addr = '127.0.0.1'
port_num = 5672

# 信息队列服务的连接和队列的创建
credentials = pika.PlainCredentials(username,pwd)
connection = pika.BlockingConnection(pika.ConnectionParameters(ip_addr, port_num, '/', credentials))
channel = connection.channel()
channel.queue_declare(queue='balance', durable=True)

message_str = 'Hello World!'
for i in range(1000000000):
    channel.basic_publish(
        exchange='',
        routing_key='balance', # 写明将信息发送给队列balance
        body=message_str, # 要发送的信息
        properties=pika.BasicProperties(delivery_mode=2, ) # 设置消息持久化（持久化第二部），将要发送的消息的属性标记为2，表示该信息持久化
    ) # 向消息队列发送一条信息
    print(" [%s] Sent 'Hello World'"%i)
connection.close()