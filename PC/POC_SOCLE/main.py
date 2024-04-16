from WebSocketClient import *
from ActivityManager import ActivityManager

class WebSocketCallback(WebSocketDelegate):

    def __init__(self, activity_manager):
        self.activity_manager = activity_manager
    
    def on_open(self):
        print("Connection opened")

    def on_message(self, message):
        self.activity_manager.select_activity_by_id(message)

    def on_error(self, error):
        print(f"Error: {error}")

    def on_close(self):
        print("Connection closed")

activity_manager = ActivityManager()
delegate = WebSocketCallback(activity_manager)
ws_client = WebSocketClient("ws://192.168.42.82:8080", delegate)
ws_client.start()