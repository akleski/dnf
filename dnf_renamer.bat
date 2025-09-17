
@echo off
REM Usage: dnf_renamer.bat old_string new_string
set "OLD_STRING=%1"
set "NEW_STRING=%2"
py dnf_renamer.py "%OLD_STRING%" "%NEW_STRING%"