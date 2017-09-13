from abc import ABCMeta, abstractmethod
from BaseResolver import BaseResolver

class VoidResolver(BaseResolver):
    __metaclass__ = ABCMeta

    @abstractmethod
    def call(self, data):
        pass

    def resolve(self, generator):
        for v in generator:
            self.call(v)
            yield v
