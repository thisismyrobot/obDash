""" obDash web app.
"""
from obdash import app, obd2_process_manager, socketapp


if __name__ == "__main__":

    # Launch the IO-limited stuff (the elm327-interface) in a separate
    # process.
    obd2_process_manager.start_process()

    # Launch the flask socketio-aware app
    socketapp.run(app, host='0.0.0.0')
