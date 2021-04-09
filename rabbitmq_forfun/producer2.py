import pika

# 连接rabbitmq服务器
with pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1')) as connection:
    channel = connection.channel()

    # 创建一个名为hello的队列
    # channel.queue_declare(queue='hello', durable=True) #持久化队列
    channel.queue_declare(queue='hello')

    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body='Hello world',
                          # 持久化队列配置
                          # properties=pika.BasicProperties(
                          #     delivery_mode=2,
                          # )
                          )

    print("发送‘{}’成功".format("Hello world"))
