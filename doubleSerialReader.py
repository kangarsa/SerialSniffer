import serial
#import serialdb
import dataParser
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-p1", "--port1", 
    action="store", type="string", default="/dev/pts/12")
parser.add_option("-b1", "--baudrate1", 
    action="store", type="int", default="9600")
parser.add_option("-t1", "--timeout1", 
    action="store", type="float", default=0.1)
parser.add_option("-f1", "--jsonfile1", 
    action="store", type="string", default="data.json")
parser.add_option("-p2", "--port2", 
    action="store", type="string", default="/dev/pts/13")
parser.add_option("-b2", "--baudrate2", 
    action="store", type="int", default="9600")
parser.add_option("-t2", "--timeout2", 
    action="store", type="float", default=0.1)
parser.add_option("-f2", "--jsonfile2", 
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

s_port1 = options.port
b_rate1 = options.baudrate
t_out1 = options.timeout
json_file1 = options.jsonfile
s_port2 = options.port
b_rate2 = options.baudrate
t_out2 = options.timeout
json_file2 = options.jsonfile
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
ser1 = serial.Serial(port=s_port1,baudrate=b_rate1,timeout=t_out1)
ser2 = serial.Serial(port=s_port2,baudrate=b_rate2,timeout=t_out2)
#db = serialdb.connect(host,user,passwd,db,unix_socket)
#cursor = db.cursor()

while True:
    rx1 = read_serial(ser1)
    rx2 = read_serial(ser2)

    lineOrd1 = ""
    lineHex1 = ""
    for byte in rx1:
        lineOrd1 += "["+str(ord(byte))+"]"
        lineHex1 += "["+str(hex(ord(byte))[2:])+"]"
    lineOrd2 = ""
    lineHex2 = ""
    for byte in rx2:
        lineOrd2 += "["+str(ord(byte))+"]"
        lineHex2 += "["+str(hex(ord(byte))[2:])+"]"
    print "RX as Ordinal:"
    print lineOrd1
    print "RX as Hexadecimal:"
    print lineHex1
    print "Suma:",dataParser.checksum(rx1[:-2])
    print "\n"
    print "RX as Ordinal:"
    print lineOrd2
    print "RX as Hexadecimal:"
    print lineHex2
    print "Suma:",dataParser.checksum(rx2[:-2])
    print "\n"
    dataParser.saveJson(dataParser.generateJson(rx1),json_file1)
    dataParser.saveJson(dataParser.generateJson(rx2),json_file2)
#    serialdb.save(db,cursor,rx)

