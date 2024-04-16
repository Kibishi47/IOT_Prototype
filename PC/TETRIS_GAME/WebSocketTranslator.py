class WebSocketTranslator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WebSocketTranslator, cls).__new__(cls, *args, **kwargs)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.isKeyDown = False
        self.isKeyUp = False
        self.isKeyLeft = False
        self.isKeyRight = False

    def calcul(self, message):
        if message == "none":
            self.initialize()
        else:
            print(message)
            partsMessage = message.split(":")
            if partsMessage[0] == "u":
                if partsMessage[1] == "true":
                    self.isKeyUp = True
                if partsMessage[1] == "false":
                    self.isKeyUp = False
            elif partsMessage[0] == "d":
                if partsMessage[1] == "GAUCHE":
                    self.isKeyLeft = True
                    self.isKeyRight = False
                if partsMessage[1] == "DROITE":
                    self.isKeyLeft = False
                    self.isKeyRight = True
                if partsMessage[1] == "MIDDLE":
                    self.isKeyLeft = False
                    self.isKeyRight = False
            elif partsMessage[0] == "b":
                if partsMessage[1] == "pressed":
                    self.isKeyDown = True
                if partsMessage[1] == "not-pressed":
                    self.isKeyDown = False
            else:
                self.initialize()

    def toJSON(self):
        return f"up:{self.isKeyUp}, down:{self.isKeyDown}, left:{self.isKeyLeft}, right:{self.isKeyRight}"

        
