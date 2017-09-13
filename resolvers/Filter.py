from BaseResolver import BaseResolver

class Filter(BaseResolver):
    def __init__(self, filter_):
        self.__filter = filter_

    def resolve(self, generator):
        for v in generator:
            if self.__filter(v):
                yield v
