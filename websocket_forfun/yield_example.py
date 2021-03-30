from time import  sleep

# 参考https://www.cnblogs.com/dhcn/p/9032461.html
class Potato:
    @classmethod
    def make(cls, num, *args, **kws):
        potatos = []
        for i in range(num):
            potatos.append(cls.__new__(cls, *args, **kws))
        return potatos

all_potatos = Potato.make(5)

def take_potatos(num): #这个是一个迭代器，通过next或者for循环能一个个的拿出元素
    count = 0
    while True:
        if len(all_potatos) == 0:
            print('等待补货')
            sleep(.1)
        else:
            potato = all_potatos.pop()
            print('拿下一个土豆放入篮子')
            yield potato
            count += 1
            if count == num:
                break

def buy_potatos():
    bucket = []
    for p in take_potatos(50):
        bucket.append(p)

buy_potatos()