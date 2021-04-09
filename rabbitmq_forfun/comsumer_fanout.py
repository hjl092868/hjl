import pika

# https://blog.csdn.net/qq_37623764/article/details/105767004

# 连接rabbitmq服务器
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()

# 创建一个名为logs的交换机（用于分布日志），模式是发布订阅模式
channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')


result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
print('随机队列名：{}'.format(queue_name))

