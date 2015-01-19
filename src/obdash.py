import config
import flask.ext.socketio
import flask
import glob
import obd2
import os
import re
import time


# Create the app
app = flask.Flask('obDash')
app.debug = config.FLASK_DEBUG
app.root_path = os.path.abspath(os.path.dirname(__file__))

# Prep for and create the socket app
app.config['SECRET_KEY'] = 'secret!'  # TODO: don't...
socketapp = flask.ext.socketio.SocketIO(app)

# The epoc offset from a client device. None indicates is has not been set.
EPOCH_OFFSET = None


def valid_app_name(name):
    return re.match('^[a-z0-9-]{1,10}$', name) is not None

# Grab a list of app names
APPS = filter(valid_app_name,
              map(os.path.basename,
                  map(os.path.dirname,
                      glob.glob(os.path.join(app.root_path,
                                             'apps', '*', 'index.html')))))


def safepath(path):
    return '..' not in path and not path.strip().startswith('/')


@socketapp.on('poll')
def handle_poll(message):
    """ Handles PID polls.
    """
    try:
        for mode, pid in message['pids']:
            socketapp.emit('value', {
                'timestamp': (None
                              if EPOCH_OFFSET is None
                              else EPOCH_OFFSET + time.time()),
                'pid': (mode, pid),
                'value': obd2.value(mode, pid),
            })
    except KeyError:
        flask.abort(418)  # "I'm a teapot" error...


@app.route("/")
def index():
    """ The main page
    """
    return flask.render_template('index.html', apps=APPS)


@app.route("/app/<appname>/<filename>")
def appresources(appname, filename):
    """ Return app-specific resources.
    """
    if not valid_app_name(appname):
        flask.abort(418)  # "I'm a teapot" error...

    if not safepath(filename):
        flask.abort(418)  # "I'm a teapot" error...

    if filename == 'index.html':
        # Redirect to app root
        return flask.redirect('/app/{}/'.format(appname), 302)

    path = os.path.join(app.root_path, 'apps', appname)

    return flask.send_from_directory(path, filename)


@app.route("/app/<name>/")
def loadapp(name):
    """ The app loader
    """
    # Apps must be lower case strings alphanumeric + underscore strings, 1-10
    # characters long.
    if not valid_app_name(name):
        return 'invalid app name'

    # Grab the template
    # Forward slash on all platforms, according to Flask docco
    # http://flask.pocoo.org/docs/0.10/api/#flask.Flask.open_resource
    app_resource_name = 'apps/{}/index.html'.format(name)
    try:
        with app.open_resource(app_resource_name) as rf:
            app_template = rf.read()
    except IOError:
        return 'failed to load app'

    # Render the template and return it
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
        flask.abort(418)  # "I'm a teapot" error...

    # Update the offset
    EPOCH_OFFSET = float(epoch) - time.time()

    return ''


if __name__ == "__main__":
    socketapp.run(app, host='0.0.0.0')
