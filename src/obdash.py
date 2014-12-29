import flask.ext.socketio
import flask
import glob
import operator
import os
import re
import subprocess


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
