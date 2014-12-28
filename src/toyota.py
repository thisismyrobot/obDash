# Flask fundamentals
from flask import Flask
app = Flask('toyota')

# Some configuration
app.config['SECRET_KEY'] = 'secret!' # TODO: don't...
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 # 10KB seems fair

# Websockets
import flask.ext.socketio
socketio = flask.ext.socketio.SocketIO(app)

@app.route("/")
def hello():
    """ The main page...
    """
    return "Hello World!"


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')
