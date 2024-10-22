#!/bin/bash

MIKHAIL_LOCATION="$HOME/mikhail"

source $MIKHAIL_LOCATION/.venv/bin/activate
python $MIKHAIL_LOCATION/src/mikhail.py $@ -macos
deactivate
