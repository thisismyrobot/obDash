import obdash.config
import flask.ext.socketio
import flask
import logging
import obdash.obd2_proc
import obdash.tools
import os


# Logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(levelname)s - [%(asctime)s] - %(name)s: %(message)s',
)

# Create the app
app = flask.Flask('obDash')
app.debug = obdash.config.FLASK_DEBUG
app.root_path = os.path.abspath(os.path.dirname(__file__))

# Prep for and create the socket app
app.config['SECRET_KEY'] = 'secret!'  # TODO: don't...
socketapp = flask.ext.socketio.SocketIO(app)

# The obd2 interface process
obd2_api = obdash.obd2_proc.Obd2Process(obdash.config.OBD2INTERFACE)

# The views need to be configured last
import obdash.views
