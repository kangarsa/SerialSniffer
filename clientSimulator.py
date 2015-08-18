# coding=utf-8
import serial
import time

s_port = "/dev/pts/9"
b_rate = 9600
t_out = 0.1

#open serial
ser = serial.Serial(port=s_port,baudrate=b_rate,timeout=t_out)

f = open('serialExample.txt', 'r')


handshake_send = [
["[aa][aa][1][0][0][0][0][4][0][1][59]","[59][aa][1][0][0][0][0][0][0][1][55]"],
["[aa][aa][1][0][0][0][0][1][b][31][31][31][31][31][31][31][31][20][20][1][3][2a]"],
["[aa][aa][1][0][0][1][1][3][0][1][5a]"],
["[aa][aa][1][0][0][1][1][0][0][1][57]"],
["[aa][aa][1][0][0][1][1][1][0][1][58]"],
["[aa][aa][1][0][0][1][1][4][0][1][5b]"]
]

handshake_recieve = [
["[aa][aa][0][0][1][0][0][80][a][31][31][31][31][31][31][31][31][20][20][3][a7]"],
["[aa][aa][0][1][1][0][0][81][1][6][1][de]"],
["[aa][aa][0][1][1][0][1][83][40][31][20][20][34][36][30][30][5a][30][2e][30][33][50][56][20][34][36][30][30][20][20][20][20][20][20][20][20][20][50][48][4f][45][4e][49][58][54][45][43][20][20][20][20][20][20][31][31][31][31][31][31][31][31][20][20][20][20][20][20][20][20][34][35][30][30][e][28]"],
["[aa][aa][0][1][1][0][1][80][1b][0][1][2][3][4][5][6][d][40][41][42][43][44][45][47][48][49][4a][4c][78][79][7a][7b][7c][7d][7e][7f][8][ed]"],
["[aa][aa][0][1][1][0][1][81][6][40][41][44][45][46][47][3][75]"],
["[aa][aa][0][1][1][0][1][84][c][5][dc][0][14][7][a8][9][e2][13][24][13][ec][5][ac]"]
]

conn_send = [
"[aa][aa][1][0][0][0][0][0][0][1][55]",
"[aa][aa][1][0][0][0][0][0][0][1][55]",
"[aa][aa][1][0][0][1][1][2][0][1][59]"
]

conn_state = 0

def read_serial(ser):
	buf = ''
	while True:
		inp = ser.read(500) #read 500 bytes or do timeout
		buf = buf + inp #accumalate the response
		if buf != '':
			return buf

while True:

	if conn_state < 2:
		conn_state = 1
		way = 0
		while way < len(handshake_send) and conn_state == 1:
			#mientras no termine las vías y la conexion este estableciendose
			for m in handshake_send[way]:
				#envio todos los mensajes de la vía actual
				print m
				ser.write(m)
			# espero mensajes de la vía actual
			rx = read_serial(ser)
			print rx
			# si el mensaje no es el esperado
			if rx != handshake_recieve[way][0]:
				# reseteo la conexion
				conn_state = 0
				print "conn_state: ", 0
			way+=1
		# si ya es el último mensaje
		if way == len(handshake_recieve) and conn_state == 1:
			# se estableció conexion correctamente
			conn_state = 2
	elif conn_state == 2:
		# establecida la conexion envio los mensajes
		# AQUI SE DEBEN COMPROBAR TIEMPOS DE ENVIO Y DE RESPUESTA CORRECTOS
		for m in conn_send:
			# envio todos los mensajes
			print m
			ser.write(m)
		rx = read_serial(ser)
		print rx

		

#	time.sleep(3)
#	f.seek(0)


