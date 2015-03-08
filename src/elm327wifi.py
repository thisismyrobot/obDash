import contextlib
import re
import socket
import time


def clean_ascii(string):
    """ Return a string with nothing but a-z0-9 in it.
    """
    return ' '.join(
        filter(None, re.sub('[^ \w.]+', ' ', string, re.IGNORECASE).split(' '))
    )


class __Reader(object):

    def __init__(self, ip='192.168.0.10', port=35000):
        self._ip = ip
        self._port = port
        self._setup_ran = False

    def do_setup(self, sock):
        # Reset
        sock.sendall('ATZ\r')

        time.sleep(5)
        sock.recv(1024)

        # Disable command echo
        sock.sendall('ATE0\r')
        sock.recv(1024)

        time.sleep(1)

        # Auto protocol
        sock.sendall('ATSP0\r')
        sock.recv(1024)

        time.sleep(1)

        # Adaptive timing Auto 1 - TODO: note what this means, I've used it
        # before though.
        sock.sendall('AT1\r')
        sock.recv(1024)

        time.sleep(1)

        print 'Setup done'#, clean_ascii(sock.recv(1024))

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
                sock.settimeout(1)
                sock.connect((self._ip, self._port))

                if not self._setup_ran:
                    self._setup_ran = True  # Otherwise we go around in circles :)
                    self.do_setup(sock)

                sock.sendall(at_command)

                # TODO: Tune this - and it's derivable from the number of
                # tokens.
                response = clean_ascii(sock.recv(1024))

                if str_response:
                    return response

                # Parse out the actual response data
                data = response.split(" ")[2:]

                # Create tokens from the data
                tokens = [ord(chr(int(t, 16))) for t in data]

                print_str = ','.join((
                    clean_ascii(at_command),
                    response,
                    str(data),
                    str(tokens),
                ))
                print print_str

                return tokens

        except Exception as e:
            print e, clean_ascii(at_command)
            return []

__reader = __Reader()
get = __reader.transact
