# Toyota code

Some sandboxing code for OBD logging and display for my little Toyota :)

# Note

Um, this is a sandbox. Nothing here is stable, but if there's something you
like, have fun with it.

# Setup

## Windows

This is just for those who want to look at it on a Windows box. *nix
instructions to follow.

In the current folder:

    pip install virtualenv
    virtualenv venv
    venv\Scripts\pip.exe install -r requirements.txt
    python src\toyota.py

# Licence

MIT except for odb2scantool folder that is GPL (snapshotted from
https://github.com/AustinMurphy/OBD2-Scantool 15/12/2014).
