import socket
# 参考 https://zhuanlan.zhihu.com/p/72040375
# dms协议要求： 采用网络方式通讯时，终端应作为通讯网络中的服务端，外设作为客户端。终端作为服务端时IP地址推荐为192.168.100.100，端口号为8888。


def check_code_transfer(ori_data):
    """
    校验码：从厂商编号到用户数据依次累加的累加和，然后取累加的低 8 位作为校验码
    :param ori_data:
    :return:
    """
    sum = 0
    for data in ori_data.split(' '):
        sum += int(data, 16)
    result = hex(sum)
    return '0x' + result[-2:]


def data_transfer(ori_data):
    """
    0x7e <————> 0x7d 后紧跟一个 0x02。
    0x7d <————> 0x7d 后紧跟一个 0x01。
    转义处理过程如下：
    发送消息时：消息封装——>计算并填充校验码——>转义。
    接收消息时：转义还原——>验证校验码——>解析消息。
    发送一包内容为 0x30 0x7e 0x08 0x7d 0x55 的数据包，则经过封装如下：0x7e 0x30 0x7d 0x02
    0x08 0x7d 0x01 0x55 0x7e
    :param ori_data:
    :return:
    """
    data_list = []
    for data in ori_data.split(' '):
        if data == '0x7e':
            data_list.append('0x7d')
            data_list.append('0x02')
        elif data == '0x7d':
            data_list.append('0x7d')
            data_list.append('0x01')
        else:
            data_list.append(data)
    return ' '.join(data_list)


def tranfer_bytes(ori_data):
    import binascii
    data_list = []
    for data in ori_data.split(' '):
        if len(data) == 6:
            data_list.append(data[2:4])
            data_list.append(data[-2:])
        else:
            data_list.append(data[-2:])
    return binascii.a2b_hex(''.join(data_list))


# AF_INET,该参数支持 socket.AF_UNIX（UNIX 网络）、socket.AF_INET（基于 IPv4 协议的网络）和 socket.AF_INET6（基于 IPv6 协议的网络）这三个常量
# SOCK_STREAM,该参数可支持 SOCK_STREAM（默认值，创建基于 TCP 协议的 socket）、SOCK_DGRAM（创建基于 UDP 协议的 socket）和 SOCK_RAW（创建原始 socket）。一般常用的是 SOCK_STREAM 和 SOCK_DGRAM
# 服务端
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(('192.168.100.101', 18888))
soc.listen()
conn, addr = soc.accept()  # conn为套接字的对象，用来发送和接收数据，addr则是连接的客户端地址

n = 0
while True:
    print(conn, addr)
    msg = conn.recv(1024)
    # 0x7e 0x?? 0x0000 0x0000 0x65 0x31 0x0000 0x000000000000 0x00000000 0x00000000 0x0000 0x0000 0x00000000 0x00 0x61 0x7e
    #                                   数据内容开始--------------------------------------------------------------结束
    # 0x7e 0x?? 0x0000 0x0000 0x65 0x31 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x61 0x7e
    #                                   数据内容开始-----------------------------------------------------------------------------------------------------------------结束

    # 发送消息时：消息封装——>计算并填充校验码——>转义
    # 忽略掉验证码，先进行转义

    # 校验码：从厂商编号到用户数据依次累加的累加和，然后取累加的低 8 位作为校验码
    if n == 0:
        ori_check_code = '0x0000 0x65 0x2f'
    else:
        ori_check_code = '0x0000 0x65 0x31 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x61' #速度
        # ori_check_code = '0x0000 0x65 0x31 0x61 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00' #速度
        ori_check_code = '0x0000 0x65 0x31 0x00 0x00 0x00 0x00 0x01 0x34 0x62 0x9b 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00' #时间
    check_code = check_code_transfer(ori_check_code)

    # ori_data = ' '.join(['0x7e', check_code, '0x0000', check_code, '0x7e'])
    ori_data = ' '.join([check_code, '0x0000', ori_check_code])
    result_data = ' '.join(['0x7e', data_transfer(ori_data), '0x7e'])
    final_result_data = tranfer_bytes(result_data)
    conn.send(final_result_data) #尝试0x31作为功能码、0x61作为速度（97km/h）、速度是不是取值为0x0000 0x000000000000 0x00000000 0x00000000 0x0000 0x0000 0x00000000 0x00 0x61
    n += 1
conn.close()
soc.close()

# while True:
#     conn, addr = soc.accept()
#     print(conn, addr)
#     msg = conn.recv(1024)
#     conn.send()
#     conn.close()


# # 客户端
# soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# soc.connect(('192.168.100.101', 8888))
# soc.send() #输入二进制
# recv = soc.recv(1024)