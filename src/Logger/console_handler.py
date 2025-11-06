import logging

class ConsoleHandler:
    
    def __init__(self,formatter:logging.Formatter):
        self.formatter = formatter
        
    def build(self):
        h = logging.StreamHandler()
        h.setFormatter(self.formatter)
        return h
    
    
        
