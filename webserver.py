from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from optparse import OptionParser
from urlparse import parse_qs
import json
#import MySQLdb
import dataParser
from pymongo import MongoClient
from bson.objectid import ObjectId

#cnx = MySQLdb.connect(host="localhost", # your host, usually localhost
#                    user="serial", # your username
#                    passwd="serial", # your password
#                    db="serial",
#                    unix_socket="/opt/lampp/var/mysql/mysql.sock") # name of the data base
# cnx = mysql.connector.connect(user='serial', password='serial', database='serial')
#cursor = cnx.cursor()

parser = OptionParser()
parser.add_option("-p", "--port", 
    action="store", type="int", default=8003)
parser.add_option("-j", "--jsonfile", 
    action="store", type="string", default="data.json")
(options, args) = parser.parse_args()

port = options.port
json_file = options.jsonfile

client = MongoClient('mongodb://localhost:27017/')
db = client.serial_database

class MyRequestHandler (BaseHTTPRequestHandler) :
    
    def do_GET(self) :
        o = parse_qs(self.path[1:])
        #send response code:
        self.send_response(200)
        #send headers:
        self.send_header("Content-type:", "text/html")
        # send a blank line to end headers:
        self.wfile.write("\n")
        #cursor = cnx.cursor()
        #with open(json_file) as data_file:    
        #    data = json.load(data_file)
        if 'actual' == self.path[1:7]:
            #send response:
            #query = ("SELECT * FROM lecturas ORDER BY id DESC LIMIT 1")
            #cursor.execute(query)
            last = db.reads.find().sort({_id:-1}).limit(1)
            print last
            response = ""
            f = open("last_data_raw")
            txt = f.read()
            response += dataParser.generateJson(txt)
            print response
            f.close()
            self.wfile.write(response)
            #for (iden,ts,value) in cursor:
            #    response = "id: {}, fecha: {:%d %b %Y}, value: {}".format(iden,ts,value)                
                #self.wfile.write(response)
            #    v = dataParser.generateJson(value)
            #    self.wfile.write(v)
            #cursor.close()
            #json.dump(data, self.wfile)
        elif 'historico' in self.path[1:10]:
            #???
            print "hola"

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

server = HTTPServer(("", port), MyRequestHandler)

server.serve_forever()