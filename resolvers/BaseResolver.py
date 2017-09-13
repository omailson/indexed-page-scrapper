from abc import ABCMeta, abstractmethod

class BaseResolver:
    __metaclass__ = ABCMeta

    @abstractmethod
    def resolve(self, generator):
        pass
