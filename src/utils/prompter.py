import os
import sys
import termios
import tty

class Option:
    def __init__(self, name: str, data=None) -> None:
        self.name = name
        self.data = data

class Action:
    def __init__(self, action, message=False) -> None:
        self.action = action

        if message == False:
            message = lambda data: f"{data}"

        self.message = message


class Prompter:
    def __init__(self, options, actions, question='Select an option'):
        self.options: list[Option] = options
        self.actions: dict[str, Action] = actions
        self.question = question

    def clear_current_line(self):
        sys.stdout.write(u'\033[K')

    def move_cursor_up(self, lines=1):
        sys.stdout.write(f'\033[{lines}A')

    def move_cursor_down(self, lines=1):
        sys.stdout.write(f'\033[{lines}B')
    
    def read_character(self):
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
        output_message = ''
        
        self.display_menu(self.options, current_option)

        key = self.read_character()

        if key == 'j' or key == u'\x1b[B':
            current_option = (current_option + 1) % len(self.options)
        elif key == 'k' or key == u'\x1b[A':
            current_option = (current_option - 1) % len(self.options)

        elif key in self.actions:
            action = self.actions[key]
            data = self.options[current_option].data
            action.action(data)
            output_message = action.message(data)

        print('\n' + output_message)

        self.move_cursor_up(len(self.options) + 2)

    
