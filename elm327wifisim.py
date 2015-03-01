""" A cheap and cheerful elm327 wifi dongle simulator.
"""
import SocketServer


LISTEN_IP = 'localhost'


RESPONDERS = {
    'ATI': lambda: 'LM327 v1.5 (fake)',
    '010C': lambda: '01 07',  # RPM
    '010D': lambda: '64',  # KPH
}


class ELM327Handler(SocketServer.BaseRequestHandler):
    def handle(self):
        command = self.request.recv(1024).strip()

        # Attempt to create the response
        response = None
        try:
            response = RESPONDERS[command]()
        except KeyError:
            # Unknown command
            pass

        # Pad the response unless it is a string response
        if command not in ('ATI',):
            response = '{} {} {} BA'.format(
                command[:2],
                command[2:4],
                response,
            )

        print '{} => {}'.format(command, response)

        if response is not None:
            self.request.sendall(response)


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = SocketServer.TCPServer((LISTEN_IP, 35000), ELM327Handler)
    server.serve_forever()
