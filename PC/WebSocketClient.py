import websocket
from threading import Thread

class WebSocketClient(Thread):
    def __init__(self, uri, delegate):
        super().__init__()
        self.uri = uri
        self.delegate = delegate
        self.ws = websocket.WebSocketApp(uri,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

    def run(self):
        self.ws.run_forever()

    def on_open(self, ws):
        if self.delegate:
            self.delegate.on_open()

    def on_message(self, ws, message):
        if self.delegate:
            self.delegate.on_message(message)

    def on_error(self, ws, error):
        if self.delegate:
            self.delegate.on_error(error)

    def on_close(self, ws):
        if self.delegate:
            self.delegate.on_close()

class WebSocketDelegate:
    def on_open(self):
        pass

    def on_message(self, message):
        pass

    def on_error(self, error):
        pass

    def on_close(self):
        pass

class MyWebSocketDelegate(WebSocketDelegate):
    def on_open(self):
        print("Connection opened")

    def on_message(self, message):
        print(f"My received: {message}")

    def on_error(self, error):
        print(f"Error: {error}")

    def on_close(self):
        print("Connection closed")

if __name__ == "__main__":
    websocket.enableTrace(True)
    uri = "ws://192.168.232.92:80"
    delegate = MyWebSocketDelegate()
    client = WebSocketClient(uri, delegate)
    client.start()
