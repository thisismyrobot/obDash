# Debug mode or not for the flask app.
FLASK_DEBUG = True

# The tty with the ELM327.
OBDTTY = '/dev/ttyUSB0'  # For testing, should be something like /dev/rfcomm0

# How many times a second to request new data, should match the max rate of
# ELM327 device
PINGRATE = 20
