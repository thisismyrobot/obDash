import flask.ext.socketio
import flask
import glob
import operator
import os
import re
import subprocess
import time


# Create the app, and the socket app to surround it
app = flask.Flask('obDash')
app.debug = True
app.root_path = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'secret!' # TODO: don't...
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 # 10KB seems fair
socketapp = flask.ext.socketio.SocketIO(app)

# Grab a list of app names
APPS = map(operator.itemgetter(0),
           map(os.path.splitext,
               map(os.path.basename,
                   glob.glob(os.path.join(app.root_path, 'apps', '*.html')))))

# The epoc offset from a client device. None indicates is has not been set.
EPOCH_OFFSET = None


@app.route("/")
def index():
    """ The main page
    """
    return flask.render_template('index.html', apps=APPS)


@app.route("/app/<name>")
def loadapp(name):
    """ The app loader
    """
    # Apps must be lower case strings alphanumeric + underscore strings, 1-10
    # characters long.
    if re.match('^\w{1,10}$', name) is None:
        return 'invalid app name'

    # Forward slash on all platforms, according to Flask docco
    # http://flask.pocoo.org/docs/0.10/api/#flask.Flask.open_resource
    app_resource_name = 'apps/{}.html'.format(name)
    try:
        with app.open_resource(app_resource_name) as rf:
            app_template = rf.read()
    except IOError:
        return 'failed to load app'

    try:
        return flask.render_template_string(app_template)
    except:
        return 'failed to render app'


@app.route("/time", methods=['GET', 'POST'])
def settime():
    """ Get the current time using a GET request, "set" it using a POST.

        GET data includes the offset used in data timestamping, from the
        device time.

        POST variable is "epoch" and is the current epoch time in seconds,
        from this and the current device time an offset is calculated and
        stored.
    """
    global EPOCH_OFFSET

    if flask.request.method == 'GET':
        now = time.time()
        return flask.jsonify({
            'dev_epoch': now,
            'data_offset': EPOCH_OFFSET,
            'data_epoch': None if EPOCH_OFFSET is None else EPOCH_OFFSET + now
        })

    # We only the POST data if we don't already have one set
    if EPOCH_OFFSET is not None:
        return

    epoch = flask.request.form.get('epoch', None)

    # It has to be a positive integer...
    try:
        if float(epoch) < 0:
            raise Exception('Negative number...')
    except:
        flask.abort(418) # "I'm a teapot" error...

    # Update the offset
    EPOCH_OFFSET = float(epoch) - time.time()

    return ''


if __name__ == "__main__":
    socketapp.run(app, host='0.0.0.0')
