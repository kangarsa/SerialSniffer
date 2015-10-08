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
        self.send_header('Access-Control-Allow-Origin', '*')
        # send a blank line to end headers:
        self.wfile.write("\n")
        #cursor = cnx.cursor()
        #with open(json_file) as data_file:    
        #    data = json.load(data_file)
        if 'actual' == self.path[1:7]:
            #send response:
            #query = ("SELECT * FROM lecturas ORDER BY id DESC LIMIT 1")
            #cursor.execute(query)
            last = db.reads.find().sort([("_id",-1)]).limit(1)
            for x in last:
                elemento = x
            response = ""
            print elemento
            #f = open("last_data_raw")
            #txt = f.read()
            txt = elemento['data']
            response += dataParser.generateJson(txt)
            print response
            #f.close()
            self.wfile.write(response)
            #for (iden,ts,value) in cursor:
            #    response = "id: {}, fecha: {:%d %b %Y}, value: {}".format(iden,ts,value)                
                #self.wfile.write(response)
            #    v = dataParser.generateJson(value)
            #    self.wfile.write(v)
            #cursor.close()
            #json.dump(data, self.wfile)
        elif 'historico' in self.path[1:10]:
            ts1 = self.path[11:21]
            ts2 = self.path[22:33]
            salto = 3600
            elementos = []
            #print ts2
            for hora in range(int(ts1),int(ts2),salto):
                id1 = ObjectId(str(hex(hora))[2:]+"0000000000000000")
                id2 = ObjectId(str(hex(hora+salto))[2:]+"0000000000000000")
                last = db.reads.find({"_id" : {"$gt":id1,"$lt":id2}}).limit(1)
                for x in last:
                    elem = dataParser.generateDict(x['data'])
                    elem["time"] = str(x['_id'].generation_time)
                    elementos.append(elem)
            #for x in range(0,last.count(),360):#int(last.count()/24)):
            #    elementos.append(dataParser.generateDict(last[x]['data']))
            response = ""
            print elementos
            #f = open("last_data_raw")
            #txt = f.read()
            txt = ""#elemento['data']
            #response += dataParser.generateJson(txt)
            response = json.dumps({"elementos":elementos}) #json.dumps({"elementos":elementos})
            print response
            #f.close()
            self.wfile.write(response)
            print "hola"

    def end_headers(self):
        http.server.SimpleHTTPRequestHandler.end_headers(self)

server = HTTPServer(("", port), MyRequestHandler)

server.serve_forever()