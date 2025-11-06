from .format_strings import FORMAT_STRINGS
import logging

class Formatter:
    def __init__(self, fmt_type:str = "advanced")->logging.Formatter:
        fmt_str = FORMAT_STRINGS.get(fmt_type, FORMAT_STRINGS["advanced"])
        self.formatter = logging.Formatter(fmt_str)

    def get(self)->logging.Formatter:
        return self.formatter
