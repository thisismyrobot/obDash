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

    def transact(self, at_command, str_response=False):
        """ Send a command.

            Command can be one or more strings or things that can be casted to
            strings. They are concatendated.

            So ATI works, as does 0x01, 0x0C
        """
        at_command = '{}\r'.format(at_command.strip())

        try:

            # Open a socket with a closing context, send the query, grab a
            # response.
            sock_type = (socket.AF_INET, socket.SOCK_STREAM)
            with contextlib.closing(socket.socket(*sock_type)) as sock:
                sock.connect((self._ip, self._port))
                sock.sendall(at_command)
                response = sock.recv(30)

                if str_response:
                    return response

                # Parse out the actual response data
                data = response.split(" ")[2:-1]

                # Create tokens from the data
                tokens = [ord(chr(int(t, 16))) for t in data]

                return tokens

        except Exception as e:
            print e, at_command


__reader = __Reader()
get = __reader.transact
