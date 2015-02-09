import contextlib
import socket
import time


class __Reader(object):

    def __init__(self, ip='192.168.0.10', port=35000):
        self._ip = ip
        self._port = port

        # Reset
        self.transact('ATZ')

        time.sleep(5)

        # Auto protocol
        self.transact('ATSP0')

        time.sleep(1)

    def transact(self, command):
        command = '{}\r'.format(command.strip())

        try:

            # Open a socket with a closing context
            sock_type = (socket.AF_INET, socket.SOCK_STREAM)
            with contextlib.closing(socket.socket(*sock_type)) as sock:
                sock.setblocking(0) # Non-blocking
                sock.connect((self._ip, self._port))
                sock.sendall(command)

        except Exception as e:
            print e, command

    def get(self, mode, pid):
        """ A niave and slow-ish getter over IP.
        """
        pass


reader = __Reader()
