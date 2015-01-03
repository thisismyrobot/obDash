# obDash

Some test code for OBD logging and display for my little Toyota.

# Note

Um, this is a sandbox. Nothing here is stable, but if there's something you
like, have fun with it :)

# Setup

## Raspbian on Raspberry Pi

Run this in the root of the clone of this repo.

```sh
sudo apt-get -y install python-dev
sudo apt-get -y install python-pip
pip install virtualenv
virtualenv venv
sudo venv/bin/pip install -r requirements.txt
venv/bin/python src/obdash.py
```

The gevent install bit takes forever...

# Licence

MIT
