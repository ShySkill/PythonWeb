import os
from http.server import HTTPServer, BaseHTTPRequestHandler

hostName = "localhost"
serverPort = 6060

class Serv(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'

        is_css = self.path.endswith('.css')
        is_javascript = self.path.endswith('.js')
        try:
            with open(os.path.join(os.path.dirname(__file__), self.path[1:]), 'rb') as file:
                self.send_response(200)
                if is_css:
                    self.send_header('Content-type', 'text/css') 
                elif is_javascript:
                    self.send_header('Content-type', 'application/javascript')
                else:
                    self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"File not found")



httpd = HTTPServer((hostName, serverPort), Serv)
if __name__ == "__main__":
    print("Server started, please open at http://%s:%s" % (hostName, serverPort))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print("Server stopped. Previous HTTPServer: " + hostName + ", " + serverPort)
