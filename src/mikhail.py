from command.setup import setup
from command.start import start
from command.refresh import refresh
from command.find import find
from command.build import build
from command.space import space
from command.clean import clean
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
        setup(is_mac_os=args.macos)
    if command == 'start':
        start(directory)
    if command == 'refresh':
        refresh()
    if command == 'find':
        find()
    if command == 'build':
        build()
    if command == 'space':
        space()
    if command == 'clean':
        clean(directory)

if __name__ == '__main__':
    main()
