import http.server
import socketserver
import functools

PORT = 8000
PATH = "./"


class HttpServer:

    def __init__(self, path, port):
        self.path = path
        self.port = port
        self.handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=path)

    def start_server(self):
        with socketserver.TCPServer(("", self.port), self.handler) as http:
            print("Serving at port", self.port)
            http.serve_forever()


if __name__ == "__main__":
    http_server = HttpServer(PATH,PORT)
    http_server.start_server()

