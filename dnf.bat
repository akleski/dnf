@echo off
REM Simple wrapper for the consolidated DNF script
REM Usage: dnf.bat <command_id>
REM   1 = Before work: exkontakt -> xk
REM   2 = After work: sxky -> exkontakt

if "%1"=="" (
    python dnf.py --help
    exit /b 1
)

python dnf.py "%1"
exit /b %ERRORLEVEL%