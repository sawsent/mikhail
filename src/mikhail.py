from config.config import *
from utils.utils import build_path as bp

import os
import argparse

def main():

    parser = argparse.ArgumentParser(prog='mikhail')

    parser.add_argument('command', choices=['start', 'refresh', 'find', 'build', 'space', 'clean', 'setup'])
    parser.add_argument('-macos', action='store_true')

    args = parser.parse_args() 

    handle(args)

def ensure_setup_done():
    if not os.path.exists(bp(BASE_DIR, '.venv')):
        print(f"mikhail is not setup! Please run 'mikhail setup' to make mikhail ready.")
        exit(1)
        

def handle(args):
    command = args.command
    directory = os.getcwd()
    if command == 'setup':
        from command.setup import setup
        setup(is_mac_os=args.macos)
    else:
        ensure_setup_done()

    if command == 'start':
        from command.start import start
        start(directory)
    if command == 'refresh':
        from command.refresh import refresh
        refresh()
    if command == 'find':
        from command.find import find
        find()
    if command == 'build':
        from command.build import build
        build()
    if command == 'space':
        from command.space import space
        space()
    if command == 'clean':
        from command.clean import clean
        clean(directory)

if __name__ == '__main__':
    main()
