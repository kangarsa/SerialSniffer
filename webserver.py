from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from optparse import OptionParser
import json

parser = OptionParser()
parser.add_option("-p", "--port", 
    action="store", type="int", default=8003)
parser.add_option("-j", "--jsonfile", 
    action="store", type="string", default="data.json")
(options, args) = parser.parse_args()

port = options.port
json_file = options.jsonfile

class MyRequestHandler (BaseHTTPRequestHandler) :
    
    def do_GET(self) :
        with open(json_file) as data_file:    
            data = json.load(data_file)
        if self.path == "/data" :
            #send response code:
            self.send_response(200)
            #send headers:
            self.send_header("Content-type:", "text/html")
            # send a blank line to end headers:
            self.wfile.write("\n")

            #send response:
            json.dump(data, self.wfile)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

server = HTTPServer(("", port), MyRequestHandler)

server.serve_forever()