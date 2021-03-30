# import pika
# #参考https://www.jianshu.com/p/76875d2381c0
#
# config = pika.ConnectionParameters(
#     host='127.0.0.1',
#     credentials=pika.PlainCredentials('test', 'test'),
# )
#
# conn = pika.BaseConnection(config)
# channel = conn.channel()
#
# channel.exchange_declare(exchange='ceshi', type='direct')
#
# channel.basic_publish(
#     exchange='ceshi',
#     routing_key='1',
#     body='Hello World!'
# )
#
# conn.close()