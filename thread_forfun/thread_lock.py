from threading import Thread
from threading import Lock

'''
最下面print的结果是2000000；
如果将两个线程中的锁给注释掉，这print的结果每次都不一样，证明在不加锁的情况下，
g_num会同时两个线程都执行，会产生错乱；
'''


g_num =  0

def work1():
    global g_num
    for i in range(1000000):
        # mutex.acquire()#加锁
        g_num+=1
        # mutex.release()#解锁

def work2():
    global g_num
    for i in range(1000000):
        # mutex.acquire()#加锁
        g_num+=1
        # mutex.release()#解锁

mutex = Lock()#创建锁

if __name__ == '__main__':
    # work1()
    # work2()
    # print('g_num:',g_num)#2000000

    t1 = Thread(target=work1)
    t2 = Thread(target=work2)
    t1.start()
    t2.start()

    t1.join()
    t2.join()
    print('g_num:', g_num)