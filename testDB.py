import serial
import serialdb
import dataParser
from optparse import OptionParser
import datetime

parser = OptionParser()
parser.add_option("-p", "--port", 
    action="store", type="string", default="/dev/pts/12")
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


#open serial
ser = serial.Serial(port=s_port,baudrate=b_rate,timeout=t_out)
db = serialdb.connect(host,user,passwd,db,unix_socket)
cursor = db.cursor()
# 3153600

ts_inicio = datetime.datetime.now()
print "inicio: ",ts_inicio

for x in range(0,10000):
    serialdb.save(db,cursor,"AAAA00010100018228014A0CE2000B08B5138E00D8FFFF000106820000191F000100000000000000000000000000000000083B")

ts_fin = datetime.datetime.now()
print "fin: ",ts_fin

print "tardo en cargar: ",ts_fin - ts_inicio

#print "tarda en cargar 3153600: ", ts_inicio - ts_fin * 3153600 / 10000



