#!/bin/bash

MIKHAIL_LOCATION="$HOME/mikhail"
exec > /dev/null 2>&1
source $MIKHAIL_LOCATION/.venv/bin/activate
exec > /dev/tty 2>&1
python $MIKHAIL_LOCATION/src/mikhail.py $@ -macos
exec > /dev/null 2>&1
deactivate
stty sane
exec > /dev/tty 2>&1
