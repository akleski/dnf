@echo off
REM Safe DNF Renamer - Prevents duplicate consecutive executions
REM Usage: dnf_safe.bat <command_id>
REM   1 = Before work: exkontakt -> xk
REM   2 = After work: sxky -> exkontakt

if "%1"=="" (
    echo Usage: dnf_safe.bat ^<command_id^>
    echo Command IDs:
    echo   1 = Before work: exkontakt -^> xk
    echo   2 = After work: sxky -^> exkontakt
    exit /b 1
)

py dnf_safe_runner.py "%1"
exit /b %ERRORLEVEL%