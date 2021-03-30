import asyncio
import websockets
import time
import json

# async def hello(uri):
#     print('b-111')
#     async with websockets.connect(uri) as websocket:
#         print('b-222')
#         await websocket.send("hello world")
#         print("< HELLO WORLD")
#         while True:
#             print('b-333')
#             recv_text = await websocket.recv()
#             print("> {}".format(recv_text))
#
# asyncio.get_event_loop().run_until_complete(hello('ws://localhost:8765'))

async def get_intouch(websocket):
    while True:
        data_dict = {
            'cmd': "BIND",
            'trainId': "123456",
        }
        await websocket.send(json.dumps(data_dict))
        response_str = await websocket.recv()
        print('111',response_str)
        return

async def accept_data(websocket):
    while True:
        recv_text = await websocket.recv()
        print('222',recv_text)

async def accept_websocket():
    async with websockets.connect("ws://192.168.20.97:8311/signal") as websocket:
        await get_intouch(websocket)

        await accept_data(websocket)
        # while True:
        #     recv_text = await websocket.recv()
        #     print(recv_text)
        #     # await asyncio.sleep(10)
        #     # time.sleep(10)

# async def accept_websocket():
#     async with websockets.connect("ws://192.168.20.153:8311/signal") as websocket:
#         while True:
#             recv_text = websocket.recv()
#             print(recv_text)
#             # await asyncio.sleep(10)
#             # time.sleep(10)

asyncio.get_event_loop().run_until_complete(accept_websocket())