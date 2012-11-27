@rem Running this file enables the po command.
@doskey po=C:\Python27\python.exe ^
        "Packages\Package Manager\Scripts\main.py" $* ^& ^
        "Packages\Package Manager\State\exit.bat"
@echo Po is ready to use.
