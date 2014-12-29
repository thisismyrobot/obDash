import flask.ext.socketio
import flask
import subprocess


app = flask.Flask('obDash')
app.debug = True
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
    epoc = flask.request.args.get('epoc', None)

    # It has to be a positive integer...
    try:
        if int(epoc) < 0:
            raise Exception('Negative int...')
    except:
        return ''

    # Works as 'pi' on an, err, Pi
    status = subprocess.call('sudo date --set=\'@{}\''.format(epoc),
                             shell=True)

    return ''


if __name__ == "__main__":
    socketapp.run(app, host='0.0.0.0')
