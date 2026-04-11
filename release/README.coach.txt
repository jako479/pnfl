PNFL
====

A bundle of tools for working with FbPro 98 / WinLogStats files:
   convert-pdb     Convert WinLogStats game stats (.pdb) into Excel
   read-gameplan   Extract plays from a game plan (.pln)
   write-gameplan  Update a game plan (.pln) from a list of plays


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


GETTING HELP
------------

Once installed, the 'pnfl' command is available from any terminal
(Command Prompt or PowerShell):

   pnfl --help                  list all commands
   pnfl <command> --help        show help for one command

Each tool below also has its own --help with full options.


TOOLS
-----

Each tool ships with an example .bat launcher in this folder,
and can also be called from a terminal.


1) convert-pdb  --  WinLogStats stats (.pdb) into Excel
   ----------------------------------------------------

   Example launcher:
      convert-pdb.bat

   Show help:
      pnfl convert-pdb --help

   Example terminal calls (game plans are optional):
      pnfl convert-pdb stats.pdb output.xlsm
      pnfl convert-pdb stats.pdb output.xlsm -d defense.pln -o offense.pln


2) read-gameplan  --  list the plays in a game plan (.pln)
   -------------------------------------------------------

   Example launcher:
      read-gameplan.bat

   Show help:
      pnfl read-gameplan --help

   Example terminal calls (--output is optional; without it the
   play list prints to the screen):
      pnfl read-gameplan offense.pln
      pnfl read-gameplan offense.pln --output plays.txt


3) write-gameplan  --  update a game plan (.pln) from a play list
   --------------------------------------------------------------

   Example launcher:
      write-gameplan.bat

   Show help:
      pnfl write-gameplan --help

   Example terminal call:
      pnfl write-gameplan offense.pln plays.txt


SETTINGS FILES
--------------

The .ini files in this folder hold tool settings (category order,
play paths, etc.). Most coaches will not need to change these.


TROUBLESHOOTING
---------------

"python is not recognized" or "pip is not recognized":
    Python was installed without the PATH option. Reinstall Python
    and check "Add Python to PATH".

install.bat shows errors:
    Make sure you have an internet connection (some packages are
    downloaded from the internet during install).
