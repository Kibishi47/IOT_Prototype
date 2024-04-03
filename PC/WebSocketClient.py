import websocket
import threading

class WebSocketDelegate:
    def __init__(self) -> None:
        pass
    def on_message(self, message):
        pass
    def on_error(self, error):
        pass
    def on_close(self):
        pass
    def on_open(self):
        pass

class WebSocketClient(threading.Thread):
    def __init__(self, url, delegate = None):
        super().__init__()
        self.url = url
        self.delegate = delegate
        self.ws = websocket.WebSocketApp(url,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self._stop_event = threading.Event()  # Créer un objet Event pour signaler l'arrêt du thread

    def on_message(self, ws, message):
        if self.delegate is not None:
            self.delegate.on_message(message)
        else:
            print(message)

    def on_error(self, ws, error):
        if self.delegate is not None:
            self.delegate.on_message(error)
        else:
            print(error)

    def on_close(self, ws, close_status_code, close_msg):
        if self.delegate is not None:
            self.delegate.on_message()
        else:
            print("### closed ###")

    def on_open(self, ws):
        if self.delegate is not None:
            self.delegate.on_message()
        else:
            print("Opened connection")

    def send_message(self, message):
        self.ws.send(message)

    def stop(self):
        self._stop_event.set()  # Définir le drapeau d'arrêt

    def run(self):
        self.ws.run_forever()

if __name__ == "__main__":
    ws_client = WebSocketClient("ws://192.168.232.92:80")
    ws_client.start()  # Démarrer le thread

    try:
        while True:
            pass
    except KeyboardInterrupt:
        ws_client.stop()  # Arrêter le thread WebSocketClient
        ws_client.join()  # Attendre la fin du thread
