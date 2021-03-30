import time
import datetime
import asyncio
import random

# 参考https://www.cnblogs.com/dhcn/p/9032461.html
# 购买番茄
class Tomato:
    @classmethod
    def make(cls, num, *args, **kws):
        tomatos = []
        for i in range(num):
            tomatos.append(cls.__new__(cls, *args, **kws))
        return tomatos

all_tomatos = Tomato.make(5)

async def take_tomatos(num):
    count = 0
    while True:
        if len(all_tomatos) == 0:
            await ask_for_tomato()
        tomato = all_tomatos.pop()
        yield tomato
        # time.sleep(1)
        await asyncio.sleep(1)
        count += 1
        print(f'将{count}个番茄装进了篮子',datetime.datetime.now())
        if count == num:
            break

async def ask_for_tomato():
    sleep_time = random.random()
    await asyncio.sleep(sleep_time)
    # time.sleep(1)
    sum = random.randint(1,10)
    print(f'经过时间{sleep_time}，入货{sum}个番茄',datetime.datetime.now())
    all_tomatos.extend(Tomato.make(sum))

async def buy_tomato():
    bucket = []
    async for p in take_tomatos(50):
        bucket.append(p)

# 购买土豆
class Potato:
    @classmethod
    def make(cls, num, *args, **kws):
        potatos = []
        for i in range(num):
            potatos.append(cls.__new__(cls, *args, **kws))
        return potatos

all_potatos = Potato.make(5)

async def take_potatos(num):
    count = 0
    while True:
        if len(all_potatos) == 0:
            await ask_for_potato()
        potato = all_potatos.pop()
        yield potato
        # time.sleep(1)
        await asyncio.sleep(1)
        count += 1
        print(f'将{count}个土豆装进了篮子',datetime.datetime.now())
        if count == num:
            break

async def ask_for_potato():
    sleep_time = random.random()
    await asyncio.sleep(sleep_time)
    # time.sleep(1)
    sum = random.randint(1,10)
    print(f'经过时间{sleep_time}，入货{sum}个土豆',datetime.datetime.now())
    all_potatos.extend(Potato.make(sum))

async def buy_potato():
    bucket = []
    async for p in take_potatos(50):
        bucket.append(p)

def main():
    loop = asyncio.get_event_loop()
    # res = loop.run_until_complete(buy_potato())
    res = loop.run_until_complete(asyncio.wait([buy_potato(),buy_tomato()]))
    loop.close()

main()