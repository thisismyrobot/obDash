""" obDash web app.
"""
from obdash import app, obd2_api, socketapp


if __name__ == "__main__":

    # Launch the IO-limited stuff (the elm327-interface) in a separate
    # process.
    obd2_api.start_process()

    # Launch the flask socketio-aware app
    socketapp.run(app, host='0.0.0.0')
