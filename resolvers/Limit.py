from BaseResolver import BaseResolver

class Limit(BaseResolver):
    def __init__(self, limit):
        self.limit = limit

    def resolve(self, generator):
        for i in range(self.limit):
            yield next(generator)
