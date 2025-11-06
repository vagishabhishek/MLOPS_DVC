import logging
import datetime
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from src.utils.get_project_root import get_project_root


    
class FileHandler:
    PROJECT_ROOT = get_project_root()
    DEFAULT_LOGS_DIR = PROJECT_ROOT/"logs"
    def __init__(self, formatter:logging.Formatter , filename = None,when = "midnight",backup_count = 7):
        self.formatter = formatter
        self.DEFAULT_LOGS_DIR.mkdir(parents=True,exist_ok=True)
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        default_file = self.DEFAULT_LOGS_DIR / f'app_{date_str}.log'
        self.filename  = Path(filename) if filename else default_file
        self.when = when
        self.backup_count = backup_count
        
    def build(self):
        h = TimedRotatingFileHandler(self.filename,when=self.when,backupCount=self.backup_count)
        h.setFormatter(self.formatter)
        return h
        
    
if __name__ == "__main__":
    print(get_project_root())
    