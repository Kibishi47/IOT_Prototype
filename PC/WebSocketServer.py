import asyncio
import websockets

class WebSocketDelegate:
    def on_connect(self, websocket, path):
        pass

    def on_error(self, websocket, error):
        pass

    def on_close(self, websocket, close_code, close_reason):
        pass

    def on_receive_message(self, websocket, message):
        pass

class WebSocketServer:
    def __init__(self, host, port, delegate):
        self.host = host
        self.port = port
        self.delegate = delegate
        self.clients = set()  # Liste pour stocker les connexions des clients

    async def handler(self, websocket, path):
        self.clients.add(websocket)  # Ajouter la connexion du client à la liste
        await self.delegate.on_connect(websocket, path)
        try:
            async for message in websocket:
                await self.delegate.on_receive_message(websocket, message)
        except websockets.exceptions.ConnectionClosedError as e:
            await self.delegate.on_close(websocket, e.code, e.reason)
        except Exception as e:
            await self.delegate.on_error(websocket, e)
        finally:
            self.clients.remove(websocket)  # Retirer la connexion du client de la liste

    async def broadcast(self, message):
        if self.clients:
            await asyncio.gather(*[client.send(message) for client in self.clients])

    def start(self):
        start_server = websockets.serve(self.handler, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        print(f"Serveur WebSocket démarré sur ws://{self.host}:{self.port}")
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    class MyWebSocketDelegate(WebSocketDelegate):
        async def on_connect(self, websocket, path):
            print(f"Nouvelle connexion établie depuis {websocket.remote_address}")

        async def on_error(self, websocket, error):
            print(f"Erreur survenue : {error}")

        async def on_close(self, websocket, close_code, close_reason):
            print(f"Connexion fermée : code {close_code}, raison : {close_reason}")

        async def on_receive_message(self, websocket, message):
            print(f"Reçu un message : {message}")
            # Envoie le message à tous les clients
            await server.broadcast(message)

    delegate = MyWebSocketDelegate()
    server = WebSocketServer("192.168.42.82", 8080, delegate)
    server.start()
