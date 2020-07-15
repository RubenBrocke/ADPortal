import socketserver
import string
import random

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        flag = "FLAG_" + ''.join([string.ascii_letters[random.randint(0, len(string.ascii_letters) - 1)] for _ in range(16)])
        self.request.sendall(bytes(flag, 'utf-8'))


HOST, PORT = "localhost", 1234
# Create the server, binding to localhost on port 9999
with socketserver.TCPServer((HOST, PORT), Handler) as server:
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
