
from config.config import *

import os
import argparse

def main():

    parser = argparse.ArgumentParser(prog='mikhail')

    parser.add_argument('command', choices=['start', 'refresh', 'find', 'build', 'space', 'clean', 'setup'])
    parser.add_argument('-macos', action='store_true')

    args = parser.parse_args() 

    handle(args)


def handle(args):
    command = args.command
    directory = os.getcwd()
    if command == 'setup':
        from command.setup import setup
        setup(is_mac_os=args.macos)
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
