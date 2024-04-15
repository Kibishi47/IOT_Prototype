import websocket
from threading import Thread
from Tester import Testable
import time

class WebSocketClient(Thread, Testable):
    def __init__(self, uri, delegate):
        super().__init__()
        self.uri = uri
        self.delegate = delegate
        self.ws = websocket.WebSocketApp(uri,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.connected = False
        self.time_ms_error = 2000

    def run(self):
        self.ws.run_forever()

    def send_message(self, message):
        self.ws.send(message)

    def on_open(self, ws):
        self.connected = True
        if self.delegate:
            self.delegate.on_open()

    def on_message(self, ws, message):
        if self.delegate:
            self.delegate.on_message(message)

    def on_error(self, ws, error):
        if self.delegate:
            self.delegate.on_error(error)

    def on_close(self, ws):
        self.connected = False
        if self.delegate:
            self.delegate.on_close()

    def test(self):
        actual_time_ms = 0
        while actual_time_ms < self.time_ms_error:
            time.sleep(0.05)
            actual_time_ms += 50
            if self.connected:
                return True
        return False

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
    uri = "ws://192.168.42.82:8080"
    client = WebSocketClient(uri, MyWebSocketDelegate())
    client.start()