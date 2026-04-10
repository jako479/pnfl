PNFL
====

A bundle of tools for working with FbPro 98 / WinLogStats files:
   convert-pdb     Convert WinLogStats game stats (.pdb) into Excel
   read-gameplan   Extract plays from a game plan (.pln)
   write-gameplan  Update a game plan (.pln) from a play list


REQUIREMENTS
------------

Python 3.10 or later.
Download from: https://www.python.org/downloads/

IMPORTANT: During Python installation, check the box that says
"Add Python to PATH". Without this, the install and run scripts
will not work.


INSTALLATION
------------

1. Extract this zip to a folder on your computer.
2. Double-click install.bat and wait for it to finish.

You only need to run install.bat once.


USAGE
-----

Each tool has its own .bat file in this folder:
   convert-pdb.bat
   read-gameplan.bat
   write-gameplan.bat

To use a tool:
1. Open the .bat file in Notepad and set your file paths.
2. Double-click the .bat file to run.

You can also run any command from a terminal:
   pnfl <command> [args...]

See the .ini files in this folder for additional settings
(category order, etc.).


TROUBLESHOOTING
---------------

"python is not recognized" or "pip is not recognized":
    Python was installed without the PATH option. Reinstall Python and
    check "Add Python to PATH".

install.bat shows errors:
    Make sure you have an internet connection (some packages are
    downloaded from the internet during install).
