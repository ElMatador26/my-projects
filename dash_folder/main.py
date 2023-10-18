# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 09:17:13 2023

@author: 2130006
"""

from quart import websocket, Quart

app = Quart(__name__)

connected_clients = set()
@app.websocket("/ws")
async def ws():
    connected_clients.add(websocket._get_current_object())
    await websocket.accept()
    try:
        while True:
            
            msg = await websocket.receive()
            for client in connected_clients:
                await client.send(msg)
                # if client != websocket._get_current_object():
                #     await client.send(msg)
    except:
        pass
    
    connected_clients.remove(websocket._get_current_object())

if __name__ == "__main__":
    app.run(port=5000)