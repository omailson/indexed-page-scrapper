from VoidResolver import VoidResolver
from helpers import value_or_callable

class Print(VoidResolver):
    def __init__(self, message):
        self.message = message

    def call(self, data):
        print value_or_callable(self.message, data)
