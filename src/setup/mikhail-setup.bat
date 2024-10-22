@echo off

set "MIKHAIL_LOCATION=%~1"

echo Removing current virtual environment in '%MIKHAIL_LOCATION%\.venv' ...
rmdir /S /Q "%MIKHAIL_LOCATION%\.venv"
echo Done.

echo Using 'python' to setup virtual environment in '%MIKHAIL_LOCATION%\.venv'

python -m venv "%MIKHAIL_LOCATION%\.venv"
call "%MIKHAIL_LOCATION%\.venv\Scripts\activate.bat"
pip install -r "%MIKHAIL_LOCATION%\requirements.txt"
deactivate
