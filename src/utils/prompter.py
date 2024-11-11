import os, sys

if os.name == 'nt':
    import msvcrt
    from colorama import init
    init()
else:
    import termios
    import tty

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m' 
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Option:
    def __init__(self, name: str, data=None) -> None:
        self.name = name
        self.data = data

class Action:
    def __init__(self, letter: str, help: str, action, quit_after=False) -> None:
        self.action = action
        self.letter = letter
        self.help = help
        self.quit_after: bool = quit_after

class Prompter:
    @classmethod
    def QUIT(cls, letter: str="q", help="Quit", action=lambda _: None) -> Action:
        return Action(letter, help, action, quit_after=True)

    def __init__(self, options, actions: list[Action], question='Select an option', highlight_color=Colors.YELLOW):
        self.options: list[Option] = options
        self.actions: dict[str, Action] = { action.letter: action for action in actions }
        self.question = question

        self.help_message = 'Help: ' + ' | '.join([ f"[{action.letter}]: {action.help}" for action in actions])
        self.highlight = highlight_color

    def clear_current_line(self):
        sys.stdout.write(u'\033[K')

    def move_cursor_up(self, lines=1):
        sys.stdout.write(f'\033[{lines}A')

    def move_cursor_down(self, lines=1):
        sys.stdout.write(f'\033[{lines}B')
    
    def read_character(self):
        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return ch

    def display_menu(self, options: list[Option], current_option):
        for i, option in enumerate(options):
            if i == current_option:
                print(self.highlight + f"> {option.name}" + Colors.ENDC)
            else:
                print(f"  {option.name}")

    def prompt(self):
        current_option = 0
        
        while True:
            self.display_menu(self.options, current_option)
            print('\n' + self.help_message)

            key = self.read_character()

            if key == 'j' or key == u'\x1b[B':
                current_option = (current_option + 1) % len(self.options)
            elif key == 'k' or key == u'\x1b[A':
                current_option = (current_option - 1) % len(self.options)

            elif key in self.actions:
                action = self.actions[key]
                option = self.options[current_option]
                action.action(option)
                if action.quit_after:
                    print()
                    return 0

            self.move_cursor_up(len(self.options) + 2)
