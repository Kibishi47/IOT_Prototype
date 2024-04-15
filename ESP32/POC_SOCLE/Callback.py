from button.ButtonDelegate import ButtonDelegate
from rfid.RfidDelegate import RfidDelegate
from WebSocketClient import WebSocketDelegate

class WebsocketCallback(WebSocketDelegate):

    def __init__(self):
        pass
    
    def on_open(self):
        print("Connection opened")

    def on_message(self, message):
        print(f"My received: {message}")

    def on_error(self, error):
        print(f"Error: {error}")

    def on_close(self):
        print("Connection closed")

class ClickButtonCallback(ButtonDelegate):
    def __init__(self, ws_client) -> None:
        super().__init__()
        self.ws_client = ws_client

    def short_click(self):
        print("short_click")

    def long_click(self):
        print("long_click")

class RfidCallback(RfidDelegate):
    def __init__(self, ws_client) -> None:
        super().__init__()
        self.ws_client = ws_client

    def rfid_detected(self, rfid_id):
        self.ws_client.send_message(rfid_id)