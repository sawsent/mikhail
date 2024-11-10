import os, sys

if os.name == 'nt':
    import msvcrt
    from colorama import init
    init()
else:
    import termios
    import tty

class Option:
    def __init__(self, name: str, data=None) -> None:
        self.name = name
        self.data = data

class Action:
    def __init__(self, letter: str, help: str, action) -> None:
        self.action = action
        self.letter = letter
        self.help = help

class Prompter:
    Q_TO_QUIT = "'q': Quit"

    def __init__(self, options, actions: list[Action], question='Select an option', quittable=True):
        self.options: list[Option] = options
        self.actions: dict[str, Action] = { action.letter: action for action in actions }
        self.question = question

        self.help_message = 'Help: ' + ' | '.join([ f"'{action.letter}': {action.help}" for action in actions]) + ' | ' + self.Q_TO_QUIT

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
                print(f"> {option.name}")
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
            elif key == 'q':
                self.move_cursor_down()
                return 1 

            elif key in self.actions:
                action = self.actions[key]
                data = self.options[current_option].data
                action.action(data)

            self.move_cursor_up(len(self.options) + 2)
