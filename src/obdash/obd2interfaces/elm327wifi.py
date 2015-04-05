import logging
import re
import socket
import time


logger = logging.getLogger('obdash.obd2interfaces.elm327wifi')


def clean_ascii(string):
    """ Return a string with nothing but a-z0-9 in it.
    """
    return ' '.join(
        filter(None, re.sub('[^ \w.]+', ' ', string, re.IGNORECASE).split(' '))
    )


class __Reader(object):

    def __init__(self, ip='192.168.0.10', port=35000):
        self._setup_ran = False
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(0.5)
        self._socket.connect((ip, port))

    def do_setup(self):
        # Reset
        self._socket.sendall('ATZ\r')

        time.sleep(10)
        self.safe_recv()

        # Disable command echo
        self._socket.sendall('ATE0\r')
        self.safe_recv()

        time.sleep(1)

        # Auto protocol
        self._socket.sendall('ATSP0\r')
        self.safe_recv()

        time.sleep(1)

        # Adaptive timing Auto 1 - TODO: note what this means, I've used it
        # before though.
        self._socket.sendall('AT1\r')
        self.safe_recv()

        time.sleep(5)

        print 'Setup done'  #, clean_ascii(sock.recv(1024))

    def safe_recv(self):
        try:
            return clean_ascii(self._socket.recv(1024))
        except:
            return ''

    def transact(self, at_command, str_response=False):
        """ Send a command.

            Command can be one or more strings or things that can be casted to
            strings. They are concatendated.

            So ATI works, as does 0x01, 0x0C
        """
        at_command = '{}\r'.format(at_command.strip())

        try:

            if not self._setup_ran:
                self._setup_ran = True  # Otherwise we go around in circles :)
                self.do_setup()

            self.safe_recv()
            self._socket.sendall(at_command)

            # TODO: Tune this - and it's derivable from the number of
            # tokens.
            response = self.safe_recv()

            # Parse out the actual response data
            data = response.split(" ")[2:]

            # Create tokens from the data
            tokens = [ord(chr(int(t, 16))) for t in data]

            return tokens

        except Exception as ex:
            logger.error('ELM327 Wifi transact failure: {}'.format(ex))
            return []


_reader_instance = None


def get(*args, **kwargs):
    global _reader_instance
    try:
        if _reader_instance is None:
            _reader_instance = __Reader()
        _reader_instance.transact(*args, **kwargs)
    except Exception as ex:
        _reader_instance = None
        logger.error('ELM327 Wifi thread failure: {}'.format(ex))
