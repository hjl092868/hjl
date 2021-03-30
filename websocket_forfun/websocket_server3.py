import asyncio
import websockets

async def echo(websocket, path):
    print(111)
    async for message in websocket:
        print(222)
        message = "I got your message: {}".format(message)
        print(333)
        await websocket.send(message)

asyncio.get_event_loop().run_until_complete(websockets.serve(echo, 'localhost', 8765))
asyncio.get_event_loop().run_forever()