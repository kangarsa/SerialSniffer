import serial
import time

s_port = "/dev/pts/12"
b_rate = 9600
t_out = 0.1

#open serial
ser = serial.Serial(port=s_port,baudrate=b_rate,timeout=t_out)

f = open('serialExample.txt', 'r')

while True:

    for line in f:
        print line
        ser.write(line)
        time.sleep(3)
    f.seek(0)

