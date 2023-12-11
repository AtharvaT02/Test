# File: counter.py

class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def decrement(self):
        if self.value > 0:
            self.value -= 1

    def get_value(self):
        return self.value
