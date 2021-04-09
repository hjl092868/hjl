import pika

# 连接rabbitmq服务器
connection =  pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()

# 创建一个名为logs的交换机（用于分布日志）， 模式是发布订阅模式
channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

message = "I am producer this is my message"

# 生产者向交换机logs赛信息message
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message
                      )

print("发送{}成功".format(message))
# 关闭连接
connection.close()