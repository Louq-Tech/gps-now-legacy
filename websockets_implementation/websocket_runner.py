import sys
sys.path.append("C:\\Users\\Path_Here")

import asyncio
from websockets.server import serve
from websocket_server_service import WebsocketServerService
import websockets

class WebsocketServer:
    def __init__(self):
        self.websocket_server_service = WebsocketServerService()

    async def websocket_manager(self, websocket):
        try:
            await asyncio.gather(
                self.websocket_server_service.websocket_sender_service(websocket),
            )
        
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed unexpectedly: {e}")

    async def connection_handling(self):
        try:
            async with serve(self.websocket_manager, "localhost", 8765, ping_timeout=1800, ping_interval=None, close_timeout=None):
                print("\033[1;32mServer turned on successfully\033[0m")
                await asyncio.Future()

        except Exception as e:
            print(f"\033[1;31mThere was a problem while turning on the server: {e}\033[0m")

    def websocket_run(self):
        try:
            asyncio.run(self.connection_handling())

        except KeyboardInterrupt:
            print(f"\033[1;32mServer turned off successfully\033[0m")

if __name__ == "__main__":
    websocket_server = WebsocketServer()
    websocket_server.websocket_run()