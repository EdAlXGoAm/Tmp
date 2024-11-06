from pick import pick
import os

class cmd_colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    CURSIVE = '\033[3m'

class CMDSelector:
    def __init__(self):
        self.title = ""
        self.options = []
        self.indicator = ">>"
        self.default_index = 0
    def select(self):
        option, index = pick(self.options, self.title, indicator=self.indicator, default_index=self.default_index)
        return option

class Terminal:
    @staticmethod
    def save_screen():
        os.system('')
        print("\033[?1049h", end="")

    @staticmethod
    def restore_screen():
        print("\033[?1049l", end="")

def create_path(path):
    # Create the mapping folder if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)
    return path