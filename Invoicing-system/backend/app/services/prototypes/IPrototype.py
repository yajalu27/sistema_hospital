from abc import ABC, abstractmethod
import copy

class IPrototype(ABC):
    @abstractmethod
    def clone(self):
        pass