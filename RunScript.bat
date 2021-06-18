@echo off
set /p id="Enter Path or Filename if exists in same directory: "
"%CD%\Python\python.exe" "%CD%\converter.py" "%id%"
pause