import serial

s_port = '/dev/pts/13'
b_rate = 9600
t_out = 0.1

#method for reading incoming bytes on serial
def read_serial(ser):
    buf = ''
    while True:
        inp = ser.read(500) #read a byte
#        print inp.encode("hex") #gives me the correct bytes, each on a newline
        buf = buf + inp #accumalate the response
        if buf != '':
            return buf

def checksum(bytes):
    suma = 0
    for b in bytes:
        suma += ord(b)
    return suma

#open serial
ser = serial.Serial(port=s_port,baudrate=b_rate,timeout=t_out)

while True:

#    command = '\x05\x06\x40\x00\x02\x05\xF6\x5C' #should come from user input
#    print "TX: "
#    ser.write(command)
    rx = read_serial(ser)

    lineOrd = ""
    lineHex = ""
    for byte in rx:
        lineOrd += "["+str(ord(byte))+"]"
        lineHex += "["+str(hex(ord(byte))[2:])+"]"
    print "RX as Ordinal:"
    print lineOrd
    print "RX as Hexadecimal:"
    print lineHex
    print "Suma:",checksum(rx[:-2])
    print "\n"