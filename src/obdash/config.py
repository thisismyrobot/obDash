# Debug mode or not for the flask app.
FLASK_DEBUG = False

# The tty with the ELM327.
OBDTTY = '/dev/ttyUSB0'  # For testing, should be something like /dev/rfcomm0

# How many times a second to request new data, should match the max rate of
# ELM327 device
PINGRATE = 20

# The module interfacing to the obd2hardware. Has to support a
# 'get(AT COMMAND, str_response=False)' method.
OBD2INTERFACE = 'obdash.obd2interfaces.elm327wifi'
