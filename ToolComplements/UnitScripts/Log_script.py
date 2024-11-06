import time
from ansi2html import Ansi2HTMLConverter
from TC_Common.SelectorCmd import cmd_colors

class Logger:
    def __init__(self, debug_creation_test_case=False, name="log.html"):
        self.log = []
        self.name = name
        self.debug_creation_test_case = debug_creation_test_case

    def print_and_log(self, message, print_prefix="", active=True):
        print(f"{print_prefix}{message}")
        if active:
            self.log.append(f"{print_prefix}{message}")
        self.save_log(self.name)

    def save_log(self, filename):
        conv = Ansi2HTMLConverter()
        html_content = conv.convert('\n'.join(self.log), full=True)
        with open(filename, 'w') as f:
            f.write(html_content)

    def print_message(self, type="INFO", function="", msg="", print_prefix="", active=True):
        if type == "INFO":
            self.print_and_log(f"{print_prefix}{msg}", active=active)
        elif type == "FATAL":
            self.print_and_log(f"{print_prefix}{cmd_colors.RED}Fatal Error.{cmd_colors.END} |{function}| {msg}", active=active)
            time.sleep(2)
        elif type == "ERROR":
            self.print_and_log(f"{print_prefix}{cmd_colors.RED}Error:{cmd_colors.END} |{function}| {msg}", active=active)
            time.sleep(1)
        elif type == "RESULT":
            self.print_and_log(f"{print_prefix}{cmd_colors.BLUE}Result:{cmd_colors.END} |{function}| {msg}", active=active)
            if self.debug_creation_test_case:
                key_to_continue = input(f"Press ENTER to continue...")
        elif type == "WARNING":
            self.print_and_log(f"{print_prefix}{cmd_colors.YELLOW}Warning:{cmd_colors.END} |{function}| {msg}", active=active)
            time.sleep(1)
        elif type == "ABORTED":
            self.print_and_log(f"{print_prefix}{cmd_colors.RED}Error (Action Aborted):{cmd_colors.END} |{function}| {msg} {cmd_colors.RED}Action Cancelled.{cmd_colors.END}", active=active)
            time.sleep(2)
        elif type == "SUCCESS":
            self.print_and_log(f"{print_prefix}{cmd_colors.GREEN}Success:{cmd_colors.END} |{function}| {msg}", active=active)
        self.save_log(self.name)

    def justprint_message(self, type="INFO", function="", msg="", print_prefix="", active=True):
        if type == "INFO":
            print(f"{print_prefix}{msg}")
        elif type == "FATAL":
            print(f"{print_prefix}{cmd_colors.RED}Fatal Error.{cmd_colors.END} |{function}| {msg}")
            time.sleep(2)
        elif type == "ERROR":
            print(f"{print_prefix}{cmd_colors.RED}Error:{cmd_colors.END} |{function}| {msg}")
            time.sleep(1)
        elif type == "RESULT":
            print(f"{print_prefix}{cmd_colors.BLUE}Result:{cmd_colors.END} |{function}| {msg}")
            if self.debug_creation_test_case:
                key_to_continue = input(f"Press ENTER to continue...")
        elif type == "WARNING":
            print(f"{print_prefix}{cmd_colors.YELLOW}Warning:{cmd_colors.END} |{function}| {msg}")
            time.sleep(1)
        elif type == "ABORTED":
            print(f"{print_prefix}{cmd_colors.RED}Error (Action Aborted):{cmd_colors.END} |{function}| {msg} {cmd_colors.RED}Action Cancelled.{cmd_colors.END}")
            time.sleep(2)
        elif type == "SUCCESS":
            print(f"{print_prefix}{cmd_colors.GREEN}Success:{cmd_colors.END} |{function}| {msg}")
    
    def justlog_message(self, type="INFO", function="", msg="", print_prefix="", active=True):
        if not active:
            return
        if type == "INFO":
            self.log.append(f"{print_prefix}{msg}")
        elif type == "FATAL":
            self.log.append(f"{print_prefix}{cmd_colors.RED}Fatal Error.{cmd_colors.END} |{function}| {msg}")
        elif type == "ERROR":
            self.log.append(f"{print_prefix}{cmd_colors.RED}Error:{cmd_colors.END} |{function}| {msg}")
        elif type == "RESULT":
            self.log.append(f"{print_prefix}{cmd_colors.BLUE}Result:{cmd_colors.END} |{function}| {msg}")
        elif type == "WARNING":
            self.log.append(f"{print_prefix}{cmd_colors.YELLOW}Warning:{cmd_colors.END} |{function}| {msg}")
        elif type == "ABORTED":
            self.log.append(f"{print_prefix}{cmd_colors.RED}Error (Action Aborted):{cmd_colors.END} |{function}| {msg} {cmd_colors.RED}Action Cancelled.{cmd_colors.END}")
        elif type == "SUCCESS":
            self.log.append(f"{print_prefix}{cmd_colors.GREEN}Success:{cmd_colors.END} |{function}| {msg}")
        self.save_log(self.name)