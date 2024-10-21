from command.start import start
from command.refresh import refresh
from command.find import find
from command.build import build
from command.space import space
from config.config import *

import os
import argparse

def main():

    parser = argparse.ArgumentParser(prog='mikhail')

    parser.add_argument('command', choices=['start', 'refresh', 'find', 'build', 'space'])

    args = parser.parse_args() 

    handle(args.command)


def handle(command):

    if command == 'start':
        start(os.getcwd())
    if command == 'refresh':
        refresh()
    if command == 'find':
        find()
    if command == 'build':
        build()
    if command == 'space':
        space()

if __name__ == '__main__':
    main()
