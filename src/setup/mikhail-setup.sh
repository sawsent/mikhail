#!/bin/bash

echo "Removing current virtual environment in '$MIKHAIL_LOCATION/.venv' ..."
rm -rf "$MIKHAIL_LOCATION/.venv"
echo "Done."

if command -v python 2>&1 >/dev/null; then
    PYTHON_EXEC=python
else
    PYTHON_EXEC=python3
fi

echo "Using '$PYTHON_EXEC' to setup virtual environment in '$MIKHAIL_LOCATION/.venv'"

$PYTHON_EXEC -m venv "$MIKHAIL_LOCATION/.venv"
source "$MIKHAIL_LOCATION/.venv/bin/activate"
pip install -r "$MIKHAIL_LOCATION/requirements.txt"
deactivate
