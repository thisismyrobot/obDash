""" The manager for a process to do OBD2 interfacing.
"""
import importlib
import logging
import multiprocessing
import obdash.obd2
import time


class Obd2Process(object):
    """ This is the process that does the hardware stuff.

        The ifacename is a path to a module that the launched process will
        import and pass to obd2.value() calls. The obd2 module will call get()
        on that module with AT commands as strings.
    """
    def __init__(self, ifacename):
        self._ifacename = ifacename
        self._parent, child = multiprocessing.Pipe()
        self._proc = multiprocessing.Process(
            target=self.runloop, args=(child,)
        )

    @property
    def obd2interface(self):
        # We import here as we can't pass the module to the process.
        mod = importlib.import_module(self._ifacename)
        return mod

    def runloop(self, pipe):
        """ The process that handles IO directly.

            Pushes objects back into a pipe, with a timestamp.
        """
        logger = logging.getLogger('obdash.obd2_proc')

        # The world's crappiest in-process "watchdog"...
        while True:
            try:
                iface = self.obd2interface
                while True:
                    # Blocking wait on data from the parent
                    mode, pid = pipe.recv()

                    try:
                        value = obdash.obd2.value(iface, mode, pid)
                    except obdash.obd2.NoValueException:
                        continue

                    pipe.send((mode, pid, value, time.time()))
            except Exception as ex:
                logger.error('OBD2 process failure for interface {}: {}'.format(
                    self._ifacename, ex)
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
