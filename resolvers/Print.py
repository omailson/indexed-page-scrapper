from BaseResolver import BaseResolver

class Print(BaseResolver):
    def __init__(self, message):
        self.message = message

    def resolve(self, generator):
        for v in generator:
            if callable(self.message):
                print self.message(v)
            else:
                print self.message
            yield v
