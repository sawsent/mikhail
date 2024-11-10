import os
import sys
import termios
import tty

options = [{
    'name': 'option1',
    'data': 'this is the data of option 1'
},
           {
    'name': 'option2',
    'data': 'this is the data of option 2'
}
           ]
actions = {
    'a': {
            'action': lambda data: f"Action A triggered! data: '{data}'",
            'message': lambda data: f"Action A triggered! data: '{data}'",
    },
    'b': {  
            'action': lambda data: f"Action B triggered! data: '{data}'",
            'message': lambda data: f"Action B triggered! data: '{data}'",
    }
}


def clear_current_line():
    sys.stdout.write(u'\033[K')

def move_cursor_up(lines=1):
    sys.stdout.write(f'\033[{lines}A')

def move_cursor_down(lines=1):
    sys.stdout.write(f'\033[{lines}B')

def get_character():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def display_menu(current_option):
    for i, option in enumerate(options):
        if i == current_option:
            print(f"> {option['name']}")
        else:
            print(f"  {option['name']}")

def lines_to_clear(options, output_message):
    return len(options) + len(output_message) % os.get_terminal_size().columns + 1

def main():
    

    current_option = 0
    output_message = ""
    
    while True:

        display_menu(current_option)

        key = get_character()

        if key == 'j' or key == u'\x1b[B':
            current_option = (current_option + 1) % len(options)
        elif key == 'k' or key == u'\x1b[A':
            current_option = (current_option - 1) % len(options)

        elif key == '\n':
            output_message = f"You selected: {options[current_option]}"
        
        elif key in actions:
            actions[key]['action'](options[current_option]['data'])
            output_message = actions[key]['message'](options[current_option]['data'])

        elif key == 'q':
            break

        print("\n" + output_message)

        move_cursor_up(len(options) + 2)

    print("\nExiting...")

if __name__ == "__main__":
    main()

