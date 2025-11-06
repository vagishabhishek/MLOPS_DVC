import logging
import inspect
import sys

from .console_handler import ConsoleHandler
from .file_handler import FileHandler
from .formatter import Formatter

class LoggerFactory:
    LEVELS = {
        "DEBUG" : logging.DEBUG,
        "INFO" : logging.INFO,
        "WARNING" : logging.WARNING,
        "ERROR" : logging.ERROR,
        "CRITICAL" :logging.CRITICAL
    }
    
    AUTO_EXEC_LEVELS = ['WARNING','ERROR','CRITICAL']
    
    def __init__(self,module = None,level = "DEBUG" , formatter_type = "advanced" ,log_file = None,handlers = ("console","file")):
        
        if module:
            self.name = module.__name__
        else:
            # Automatically detect the caller module
            frame = inspect.stack()[1]
            caller_module = inspect.getmodule(frame[0])
            self.name = caller_module.__name__ if caller_module else "__main__"
        
        self.level = self.LEVELS.get(level.upper(),logging.DEBUG)
        self.formatter_type = formatter_type
        self.log_file = log_file
        self.handlers = handlers
    
    
    def create(self):
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        logger.handlers.clear()
        
        formatter = Formatter(self.formatter_type).get()
        
        if "console" in self.handlers:
            logger.addHandler(ConsoleHandler(formatter).build())
            
        if "file" in self.handlers:
            logger.addHandler(FileHandler(formatter,self.log_file).build())
            
            
        for lvl_name in self.AUTO_EXEC_LEVELS:
            original = getattr(logger,lvl_name.lower())
            
            def make_wrapper(orig_func):
                def wrapper(msg, *args, **kwargs):
                    if "exc_info" not in kwargs and sys.exc_info()[0] is not None:
                        kwargs["exc_info"] = True
                    orig_func(msg, *args, **kwargs)
                return wrapper

            setattr(logger, lvl_name.lower(), make_wrapper(original))

        return logger
    
# ---------------------------
# USAGE EXAMPLE
# ---------------------------
if __name__ == "__main__":
    logger = LoggerFactory(level="DEBUG", formatter_type="advanced", handlers=("file","console")).create()

    logger.info("Application started")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.error("Something went wrong")


            