@echo off
set CWD=%~dp0
set path=%CWD%platform-tools;%path%
python auto.py
pause