@echo off
c:\python27\python.exe "%~f0\..\..\Scripts\main.py" %*
if not exist ..\State\exit.bat goto end
..\state\exit.bat
del ..\state\exit.bat
:end
