from abc import ABCMeta, abstractmethod
from copy import copy

from BaseResolver import BaseResolver

class SimpleResolver(BaseResolver):
    def resolve(self, generator):
        for v in generator:
            yield self.resolveData(copy(v))

    @abstractmethod
    def resolveData(self, data):
        pass
