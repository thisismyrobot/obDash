# Toyota code

Some sandboxing code for OBD logging and display for my little Toyota :)

# Note

Um, this is a sandbox. Nothing here is stable, but if there's something you
like, have fun with it.

# Setup

## Rasbian on Raspberry Pi

Run this in the root of the clone of this repo.

    sudo apt-get -y install python-pip
    sudo pip install virtualenv
    virtualenv venv
    venv/bin/pip install -r requirements.txt
    venv/bin/python src/toyota.py

## Windows

This is just for those who want to look at it on a Windows box.
In the current folder:

    pip install virtualenv
    virtualenv venv
    venv\Scripts\pip.exe install -r requirements.txt
    venv\Scripts\python.exe src\toyota.py

# Licence

MIT except for odb2scantool folder that is GPL (snapshotted from
https://github.com/AustinMurphy/OBD2-Scantool 15/12/2014).
