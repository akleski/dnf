
@echo off
REM Usage: dnf_renamer.bat mode old_string new_string
set "MODE=%1"
set "OLD_STRING=%2"
set "NEW_STRING=%3"
py dnf_renamer.py "%MODE%" "%OLD_STRING%" "%NEW_STRING%"