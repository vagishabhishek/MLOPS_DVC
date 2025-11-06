
from abc import ABC
from abc import abstractmethod

class BaseLoader(ABC):
    
    @abstractmethod
    def read(self, source:str):
        """Read raw data from source. Must be implemented by subclasses."""
        raise NotImplementedError
    


 