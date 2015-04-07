""" The manager for a process to do OBD2 interfacing.
"""
import importlib
import logging
import multiprocessing
import obdash.obd2
import time


class BlockingOBD2Exception(Exception):
    """ Exception to raise when something goes wrong that took some time.
    """
    pass


class Obd2Process(object):
    """ This is the process that does the hardware stuff.

        The ifacename is a path to a module that the launched process will
        import and pass to obd2.value() calls. The obd2 module will call get()
        on that module with AT commands as strings.
    """
    def __init__(self, ifacename):
        self._parent, child = multiprocessing.Pipe()
        self._proc = multiprocessing.Process(
            target=self.runloop, args=(child, ifacename)
        )

    def runloop(self, pipe, ifacename):
        """ The process that handles IO directly and runs in a sub-process.

            Pushes objects back into a pipe, with a timestamp.
        """
        logger = logging.getLogger('obdash.obd2_proc')

        # The world's crappiest in-process "watchdog"...
        while True:
            try:
                iface = importlib.import_module(ifacename)
                while True:
                    # Blocking wait on data from the parent (web) process.
                    mode, pid = pipe.recv()

                    # Attempt to retrieve the value requested by the parent
                    # process and send it back up the pipe.
                    try:
                        value = obdash.obd2.value(iface, mode, pid)

                    # Trap exceptions that result from hardware blocking
                    # timeouts. These are slow and in the meantime it's
                    # expected that a number of requests would have entered
                    # the pipe. We want to ensure the pipe doesn't overflow if
                    # (for instance) the wifi elm327 isn't plugged in for an
                    # hour so we trap these errors specifically.
                    except BlockingOBD2Exception as bex:
                        logger.error(
                            'OBD2 value(...) blocking failure: {} {} {}'.format(
                                mode, pid, bex
                            )
                        )

                        # We flush the pipe as it's expected that the
                        # exception blocked for a while before being raised.
                        count = 0
                        while pipe.poll():
                            pipe.recv()
                            count += 1
                        logger.error(
                            'Flushed {} items from request pipe'.format(count)
                        )
                        continue

                    except Exception as ex:
                        logger.error(
                            'OBD2 value(...) failure for: {} {} {}'.format(
                                mode, pid, ex
                            )
                        )
                        continue

                    pipe.send((mode, pid, value, time.time()))
            except Exception as ex:
                logger.error('OBD2 process failure for interface {}: {}'.format(
                    ifacename, ex)
                )
                time.sleep(5)

    def start_process(self):
        """ Start the process.
        """
        self._proc.start()

    def request(self, mode, pid):
        """ Helper for passing request to the process.
        """
        # Let the process know there is a new request
        self._parent.send((mode, pid))

    def response(self):
        """ Helper for reading from the remote process
        """
        if not self._parent.poll():
            return
        return self._parent.recv()
