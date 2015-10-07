import serial
#import serialdb
import dataParser
from optparse import OptionParser
from pymongo import MongoClient
from bson.objectid import ObjectId

parser = OptionParser()
parser.add_option("-p", "--port", 
    action="store", type="string", default="/dev/ttyS0")
parser.add_option("-b", "--baudrate", 
    action="store", type="int", default="9600")
parser.add_option("-t", "--timeout", 
    action="store", type="float", default=0.1)
parser.add_option("-f", "--jsonfile", 
    action="store", type="string", default="data.json")
parser.add_option("-l", "--hostdb", 
    action="store", type="string", default="localhost")
parser.add_option("-u", "--userdb", 
    action="store", type="string", default="serial")
parser.add_option("-i", "--passworddb", 
    action="store", type="string", default="serial")
parser.add_option("-n", "--database", 
    action="store", type="string", default="serial")
parser.add_option("-s", "--unixsocket", 
    action="store", type="string", default="/opt/lampp/var/mysql/mysql.sock")

(options, args) = parser.parse_args()

s_port = options.port
b_rate = options.baudrate
t_out = options.timeout
json_file = options.jsonfile
host = options.hostdb
user = options.userdb
passwd = options.passworddb
db = options.database
unix_socket = options.unixsocket

#method for reading incoming bytes on serial
def read_serial(ser):
    buf = ''
    while True:
        inp = ser.read(500) #read 500 bytes or do timeout
        buf = buf + inp #accumalate the response
        if buf != '':
            return buf

#open serial
ser = serial.Serial(port=s_port,baudrate=b_rate,timeout=t_out)
#db = serialdb.connect(host,user,passwd,db,unix_socket)
#cursor = db.cursor()

client = MongoClient('mongodb://localhost:27017/')
db = client.serial_database

while True:
    rx = read_serial(ser)
    #lineOrd = ""
    lineHex = ""
    for byte in rx:
        #lineOrd += "["+str(ord(byte))+"]"
        lineHex += "["+str(hex(ord(byte))[2:])+"]"
    #print "RX as Ordinal:"
    #print lineOrd
    print "RX as Hexadecimal:"
    print lineHex
    print "Suma:",dataParser.checksum(rx[:-2])
    print "\n"
    #db.reads

    db.reads.update(
            { "_id": ObjectId() },
            { "data": lineHex },
            upsert=True
        )

    #find().sort({_id:1}).limit(50);

    #dataParser.saveJson(dataParser.generateJson(rx),json_file)
    #serialdb.save(db,cursor,rx)

