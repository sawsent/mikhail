from config.config import *
from utils.utils import build_path as bp

import os
import argparse

def main():

    parser = argparse.ArgumentParser(prog='mikhail')

    subparsers = parser.add_subparsers(dest="command", help="Subcommands for mikhail")
    parser.add_argument('-macos', action='store_true')

    subparsers.add_parser("setup", help="Setup mikhail virtual environment and install all dependencies.")

    start_parser = subparsers.add_parser("start", help="Start mikhail in current directory, indexing all files.")
    start_parser.add_argument("-f", "--force", action='store_true', help="Forcefully remove existing mikhail folder in current dir before restarting.")

    subparsers.add_parser("clean", help="Clean all mikhail-related files in current directory, including output words and sentences.")

    subparsers.add_parser("refresh", help="Search for new audio files to index in current directory. Doesn't compromise existing transcripts and output files.")

    list_parser = subparsers.add_parser("list", help="List all words in current directory. Needs to be started")
    list_parser.add_argument("-m", "--min", default=1, help="Only show results with more than [min] occurences", type=check_positive_int)

    find_parser = subparsers.add_parser("find", help="Find a word in current directory.")
    find_parser.add_argument("word", help="Word to find.")

    info_parser = subparsers.add_parser("info", help="Display information about the health and state of mikhail.")
    info_parser.add_argument("-t", "--type", default="all", choices=["all", "general", "local"], help="What information to display.")

    args = parser.parse_args() 
    handle(args)

def check_positive_int(value):
    try:
        value = int(value)
        if value < 0:
            raise argparse.ArgumentTypeError(f"{value} is not a positive integer.")
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer.")
    return value

def is_setup() -> bool:
    return os.path.exists(bp(BASE_DIR, '.venv'))

def ensure_setup_done():
    if not is_setup():
        print(f"mikhail is not setup! Please run 'mikhail setup' to make mikhail ready.")
        exit(1)

def is_started(directory) -> bool:
    return os.path.exists(bp(directory, LOCAL_DIR))

def ensure_started(directory, command):
    if not is_started(directory):
        print(f"Mikhail needs to be started in current directory to run '{command}'. Run 'mikhail start' before 'mikhail {command}'")
        exit(1)

def handle(args):
    command = args.command
    directory = os.getcwd()
    if command == 'setup':
        from command.setup import setup
        setup(is_mac_os=args.macos)
        exit(0)

    elif command == 'info':
        from command.show_info import show_info
        show_info(directory, is_setup, is_started)


    ensure_setup_done()

    # No start needed
    if command == 'start':
        from command.start import start
        print(f"Starting mikhail in '{directory}'")
        start(directory, force=args.force)
        exit(0)

    if command == 'clean':
        from command.clean import clean
        clean(directory)
        exit(0)
    
    # start needed
    ensure_started(directory, command)

    if command == 'list':
        from command.list_words import list_words
        list_words(directory, args.min)

    if command == 'refresh':
        from command.refresh import refresh
        refresh()

    if command == 'find':
        from command.find import find
        find(directory, args.word)

    if command == 'build':
        from command.build import build
        build()

    if command == 'space':
        from command.space import space
        space()
    

if __name__ == '__main__':
    main()
