import pika

# 连接rabbitmq服务器
connection = pika.BlockingConnection(pika.ConnectionParameters(host='1270.0.01'))
channel = connection.channel()

# 两边谁先启动谁创建队列
# channel.queue_declare(queue='hello', durable=True) # 持久化队列
channel.queue_declare(queue='hello')

# 一旦有消息就执行该回调函数(比如减库操作就在这里面)
def callback(ch, method, properties, body):
    print("消费者端收到来自消息队列中的{}成功".format(body))

    # 数据处理完成，MQ收到这个应答就会删除消息
    ch.basic_ack(delivery_tag=method.delivery_tag)

# 消费者这边监听的队列是hello，一旦有值出现，则出发回调函数callback
channel.basic_consume(queue='hello',
                      auto_ack=False, # 默认就是False，可以直接不写
                      on_message_callback=callback,
)


print('当前MQ简单模式正在等待生产者往消息队列赛消息........要退出请按CTRL+C.........')
channel.start_consuming()