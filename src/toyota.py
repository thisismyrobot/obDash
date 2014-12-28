import flask.ext.socketio
import flask


app = flask.Flask('toyota')
app.config['SECRET_KEY'] = 'secret!' # TODO: don't...
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 # 10KB seems fair
socketapp = flask.ext.socketio.SocketIO(app)


@app.route("/")
def index():
    """ The main page
    """
    return flask.render_template('index.html')


@app.route("/time")
def settime():
    """ Set the current time using a GET request.
    """


if __name__ == "__main__":
    socketapp.run(app, host='0.0.0.0')
