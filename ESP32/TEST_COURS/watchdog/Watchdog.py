class Watchdog:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Watchdog, cls).__new__(cls, *args, **kwargs)
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        self.canRun = True
        self.logs = []
        self.timeManagers = []

    def get_log_array(self):
        return self.logs
    
    def get_log_str(self):
        return '\n'.join(self.logs)
    
    def get_last_log(self):
        return self.logs[len(self.logs) - 1]