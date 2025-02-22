@echo off
title OSINT Toolkit
color 0a
echo Starting OSINT Toolkit...
echo.
python -m pip install -r requirements.txt
echo.
python osint_toolkit.py
pause
