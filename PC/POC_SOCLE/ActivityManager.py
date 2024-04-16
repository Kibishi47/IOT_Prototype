class ActivityManager:
    def __init__(self) -> None:
        self.activities = {
            "360358587411": "Partie de Belotte",
            "1045908860124": "Partie de Scrabble",
            "358203173389": "Petite balade"
        }

    def select_activity_by_id(self, id):
        if id in self.activities:
            print(self.activities[id])
        else:
            print("This id is unknown")