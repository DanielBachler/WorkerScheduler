# Worker Scheduler

A project management application designed for [Milliman](https://us.milliman.com/) as a senior design
project at Montana State Univeristy.

## Required development tools

* JetBrains PyCharm with Anaconda Plugin
* Anaconda Navigator
* PyQt5
* Oracle's mySQL connector for Python
* PyInstaller

## Build Instructions

The Work Scheduler may be built using the `build-win.bat` script on any Windows machine. Your shell must
have the correct Anaconda virtual environment set up and launched. The output executable will be located
in a created `dist/` directory.

macOS and Linux users may build the project in a compatible environment with the command `pyinstaller -F work_scheduler.py`

## Running the application

If it is your first time running the application, launch it from a shell with the argument `fresh`, which will
create the appropriate database schema on login. After the application has completed its initial configuration,
you may continue use as normal. You may also launch the application without a shell or any arguments.
