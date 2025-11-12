# src/logger.py
import logging
from pathlib import Path
from datetime import datetime
import inspect

def get_project_root() -> Path:
    """Detect project root by finding .git or uv.lock"""
    current = Path.cwd()
    for parent in current.parents:
        if(parent / "uv.lock").exists():
            return parent
    return current

# === Global setup (only runs once) ===

# Common formatter — includes filename and function name
FORMATTER = logging.Formatter(
    fmt=(
        "%(asctime)s | %(levelname)-8s | %(name)s | "
        "%(filename)s:%(funcName)s:%(lineno)d | %(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S",
)

# --- Generate the RUN Folder Path ONCE upon import ---
ROOT = get_project_root()
LOGS_DIR = ROOT / "Logs"
LOGS_DIR.mkdir(exist_ok=True)

# Generate a single timestamp for the entire run
RUN_FOLDER_NAME = str(datetime.now().strftime('%d-%m-%Y %H-%M-%S'))
# Create the specific folder for this run
CURRENT_RUN_LOG_FOLDER = LOGS_DIR / RUN_FOLDER_NAME
Path.mkdir(CURRENT_RUN_LOG_FOLDER, parents=True, exist_ok=True)


def setup_logger(name: str = __name__) -> logging.Logger:
    """
    Return a logger with standard config. 
    The log files will all go into the single CURRENT_RUN_LOG_FOLDER.
    """
     # Determine the name of the calling module
    stack = inspect.stack() 
    # stack[0] is setup_logger, stack[1] is the function that called setup_logger
    
    # The FrameInfo object has a 'frame' attribute which is the actual frame object
    caller_frame = stack[1].frame 
    
    # Now you can use the correct frame object with getmodule or f_code
    caller_module = inspect.getmodule(caller_frame)
    
    # OR you can simplify the logic to get the filename
    if caller_module is not None and caller_module.__file__ is not None:
        log_filename = f"{Path(caller_module.__file__).stem}.log"
    else:
        # Fallback using the 'filename' attribute of the FrameInfo object if module detection fails
        log_filename = f"{Path(stack[1].filename).stem}.log"
    # Use the globally defined RUN folder path
    LOG_FILE_PATH = CURRENT_RUN_LOG_FOLDER / log_filename 

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(FORMATTER)

        # Use the dynamic log file path inside the *single* run folder
        file_handler = logging.FileHandler(LOG_FILE_PATH, mode='a', encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(FORMATTER)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
