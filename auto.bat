@echo off
set CWD=%~dp0
set path=%CWD%platform-tools;%path%
set path=%CWD%Python27\Scripts;%path%
set path=%CWD%Python27;%path%
python auto.py
pause