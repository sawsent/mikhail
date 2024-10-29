@echo off

if "%~1" == "setup" (
    python %~dp0mikhail.py %*
) else (
    call %~dp0..\.venv\Scripts\activate > nul 2>&1
    python %~dp0mikhail.py %*
    deactivate > nul 2>&1 
)