""" obDash web app.
"""
import obdash.config
import flask.ext.socketio
import flask
import glob
import logging
import obdash.obd2_proc
import obdash.tools
import os
import time

# Logging
#logging.getLogger('').addHandler(logging.StreamHandler())
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

# The epoc offset from a client device. None indicates is has not been set.
EPOCH_OFFSET = None

# The hardware-bound stuff will be in a different process, using shared
# memory to buffer PID values.
obd2 = None

# Grab a list of app names
APPS = filter(obdash.tools.valid_app_name,
              map(os.path.basename,
                  map(os.path.dirname,
                      glob.glob(os.path.join(app.root_path,
                                             'apps', '*', 'index.html')))))


@socketapp.on('poll')
def handle_poll(message):
    """ Handles PID polls.
    """
    for mode, pid in message['pids']:
        obd2.request(mode, pid)


@socketapp.on('tick')
def handle_tick():
    """ Handles tick requests.

        Every time a tick message is sent any data queued from the OBD
        interface is returned to the user in a series of emit messages.
    """
    while True:
        try:
            mode, pid, value, when = obd2.response()
        except TypeError:
            # If there are no responses yet/left.
            break

        socketapp.emit(
            'value', {
                'timestamp': (when
                              if EPOCH_OFFSET is None
                              else EPOCH_OFFSET + when),
                'pid': (mode, pid),
                'value': value,
            }
        )


@app.route("/")
def index():
    """ The main page
    """
    return flask.render_template('index.html', apps=APPS)


@app.route("/app/<appname>/<filename>")
def appresources(appname, filename):
    """ Return app-specific resources.
    """
    if not obdash.tools.valid_app_name(appname):
        flask.abort(418)  # "I'm a teapot" error...

    if not obdash.tools.safepath(filename):
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
    if not obdash.tools.valid_app_name(name):
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
        return ''

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
    # Launch the IO-limited stuff (the elm327-interface) in a separate
    # process.
    obd2 = obdash.obd2_proc.Obd2Process(obdash.config.OBD2INTERFACE)
    obd2.start_process()

    # Launch the flask socketio-aware app
    socketapp.run(app, host='0.0.0.0')
