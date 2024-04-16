import random

class MemoryDelegate:
    def __init__(self) -> None:
        pass

    def memory_finished(self):
        pass

class MemoryManager:
    def __init__(self) -> None:
        self.id_list = [
            "360358587411",
            "1045908860124",
            "907969735726",
        ]
        self.sentences = [
            [
                "Les fleurs",
                "dansent doucement",
                "dans le vent.",
            ],
            [
                "Le soleil",
                "éclaire la terre",
                "de sa lumière chaude.",
            ],
            [
                "Les vagues",
                "caressent le rivage",
                "avec grâce.",
            ]
        ]
        self.guess_sentence = {}
        self.actual_guess = 0

    def select_random_sentence(self):
        sentence = self.sentences[random.randint(0, len(self.sentences)-1)]
        random.shuffle(self.id_list)

        for i in range(len(self.id_list)):
            self.guess_sentence[self.id_list[i]] = sentence[i]

        print(self.guess_sentence)

    def say_part(self, id):
        sentence = self.sentences[self.actual_sentence]
        part = sentence[id]
        # SAY

    def guess(self, id):
        if self.guess_sentence:
            keys = list(self.guess_sentence.keys())
            if keys[self.actual_guess] == id:
                self.actual_guess += 1
                finished = self.check_finished()
                return True, finished
        return False, False

    def check_finished(self):
        return self.actual_guess >= len(self.id_list)
    
    def reset(self):
        self.actual_guess = 0
        self.guess_sentence = {}

if __name__ == "__main__":
    mm = MemoryManager()
    mm.select_random_sentence()