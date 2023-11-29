from http.server import BaseHTTPRequestHandler, HTTPServer
import signal
import sys

def sighandler(signum, frame):
   sys.exit()

signal.signal(signal.SIGINT, sighandler)

hostName = "localhost"

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


def run(port):
    webServer = HTTPServer((hostName, port), MyServer)


    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        sys.exit()
        pass
 

    webServer.server_close()
    print("Server stopped.")    