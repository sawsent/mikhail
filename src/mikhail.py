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

    find_parser = subparsers.add_parser("find", help="Find a word in current directory.")
    find_parser.add_argument("word", help="Word to find.")


    args = parser.parse_args() 
    handle(args)

def ensure_setup_done():
    if not os.path.exists(bp(BASE_DIR, '.venv')):
        print(f"mikhail is not setup! Please run 'mikhail setup' to make mikhail ready.")
        exit(1)

def is_started(directory):
    return os.path.exists(bp(directory, LOCAL_DIR))

def ensure_started(directory, command):
    if not is_started(directory):
        print(f"Mikhail needs to be started in current directory to find word. Run 'mikhail start' before 'mikhail {command}'")
        exit(1)

def handle(args):
    command = args.command
    directory = os.getcwd()
    if command == 'setup':
        from command.setup import setup
        setup(is_mac_os=args.macos)
        exit(0)
    else:
        ensure_setup_done()

    # No start needed
    if command == 'start':
        from command.start import start
        if is_started(directory) and args.force:
            from command.clean import clean
            print(f"Cleaning mikhail in '{directory}'")
            clean(directory)
            print("\n")
        print(f"Starting mikhail in '{directory}'")
        start(directory)
        exit(0)

    if command == 'clean':
        from command.clean import clean
        clean(directory)
        exit(0)
    
    # start needed
    ensure_started(directory, command)

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
