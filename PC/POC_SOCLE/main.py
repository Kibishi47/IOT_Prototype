from WebSocketClient import *
from ActivityManager import ActivityManager
from MemoryManager import *

class WebSocketCallbackActivity(WebSocketDelegate):

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


class WebSocketCallbackMemory(WebSocketDelegate):

    def __init__(self):
        self.memory_manager = MemoryManager()
    
    def on_open(self):
        print("Connection opened")
        self.memory_manager.select_random_sentence()

    def on_message(self, message):
        good_guess, finished = self.memory_manager.guess(message)
        if good_guess:
            if finished:
                print("Vous avez gagné")
                self.memory_manager.reset()
            else:
                print("Trouvé")
        else:
            print("Raté")

    def on_error(self, error):
        print(f"Error: {error}")

    def on_close(self):
        print("Connection closed")

activity_manager = ActivityManager()
delegate = WebSocketCallbackActivity(activity_manager)


# delegate = WebSocketCallbackMemory()

ws_client = WebSocketClient("ws://192.168.42.82:8080", delegate)
ws_client.start()