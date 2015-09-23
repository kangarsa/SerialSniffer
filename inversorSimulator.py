# coding=utf-8
import serial
import time
import binascii


def read_serial(ser):
  buf = ''
  while True:
    inp = ser.read(500) #read 500 bytes or do timeout
    buf = buf + inp #accumalate the response
    if buf != '':
      return buf

class InversorSimulator () :
  state = 0
  msg_index = 0
  port = "/dev/ttyS0"
  baud_rate = 9600
  timeout = 0.1
  handshake_finished = False

  strategy = "static"

  reset_msg = "[aa][aa][1][0][0][0][0][4][0][1][59]"

  handshake_monitor = [
  "[aa][aa][1][0][0][1][1][2][0][1][59]",
  "[59][aa][1][0][0][0][0][0][0][1][55]",
  "[aa][aa][1][0][0][0][0][1][b][31][31][31][31][31][31][31][31][20][20][1][3][2a]",
  "[aa][aa][1][0][0][1][1][3][0][1][5a]",
  "[aa][aa][1][0][0][1][1][0][0][1][57]",
  "[aa][aa][1][0][0][1][1][1][0][1][58]",
  "[aa][aa][1][0][0][1][1][4][0][1][5b]"
  ]

  monitor_messages = [
  "[aa][aa][1][0][0][0][0][4][0][1][59]",
  "[aa][aa][1][0][0][1][1][2][0][1][59]",
  "[59][aa][1][0][0][0][0][0][0][1][55]",
  "[aa][aa][1][0][0][0][0][1][b][31][31][31][31][31][31][31][31][20][20][1][3][2a]",
  "[aa][aa][1][0][0][1][1][3][0][1][5a]",
  "[aa][aa][1][0][0][1][1][0][0][1][57]",
  "[aa][aa][1][0][0][1][1][1][0][1][58]",
  "[aa][aa][1][0][0][1][1][4][0][1][5b]"
  ]

  handshake_inversor = [
  "[aa][aa][0][0][1][0][0][80][a][31][31][31][31][31][31][31][31][20][20][3][a7]",
  "[aa][aa][0][1][1][0][0][81][1][6][1][de]",
  "[aa][aa][0][1][1][0][1][83][40][31][20][20][34][36][30][30][5a][30][2e][30][33][50][56][20][34][36][30][30][20][20][20][20][20][20][20][20][20][50][48][4f][45][4e][49][58][54][45][43][20][20][20][20][20][20][31][31][31][31][31][31][31][31][20][20][20][20][20][20][20][20][34][35][30][30][e][28]",
  "[aa][aa][0][1][1][0][1][80][1b][0][1][2][3][4][5][6][d][40][41][42][43][44][45][47][48][49][4a][4c][78][79][7a][7b][7c][7d][7e][7f][8][ed]",
  "[aa][aa][0][1][1][0][1][81][6][40][41][44][45][46][47][3][75]",
  "[aa][aa][0][1][1][0][1][84][c][5][dc][0][14][7][a8][9][e2][13][24][13][ec][5][ac]"
  ]

  responses = {
  "[aa][aa][1][0][0][1][1][2][0][1][59]" : 0,
  "[aa][aa][1][0][0][0][0][0][0][1][55]" : 0,
  "[aa][aa][1][0][0][0][0][1][b][31][31][31][31][31][31][31][31][20][20][1][3][2a]" : 1,
  "[aa][aa][1][0][0][1][1][3][0][1][5a]" : 2,
  "[aa][aa][1][0][0][1][1][0][0][1][57]" : 3,
  "[aa][aa][1][0][0][1][1][1][0][1][58]" : 4,
  "[aa][aa][1][0][0][1][1][4][0][1][5b]" : 5
  }

  def iniciarlizar(self, port, baud_rate, timeout):
    print "iniciando inversor..."
    self.port = port
    self.baud_rate = baud_rate
    self.timeout = timeout
    state = 0
    self.serial = serial.Serial(port=port,baudrate=baud_rate,timeout=timeout)
    print "abrio el puerto"
    return ""

  def getHandshakeMessageFor(self, msg):
    if msg in self.handshake_monitor:
      #return self.handshake_inversor[self.handshake_monitor.index(msg)]
      return self.responses[msg]
    else:
      print "error de handshake, no es mensaje valido. Desconectando..."
      self.state = 0
      self.msg_index = 0
      return ""

  def getMessageFor(self, msg):
    response = ""
    if self.strategy == "static":
      print "buscando mensaje para responder..."
      #get index of spected message and return corresponding
      response = "AAAA00010100018228014A0CE2000B08B5138E00D8FFFF000106820000191F000100000000000000000000000000000000083B"
    if self.strategy == "dynamic":
      print "generando mensaje que responder..."
      #check msg type and generate new msg with random values
    return response

  def processMessage(self, msg):
    if msg == self.reset_msg:
      print "estado actual desconectado, recibido mensaje de reconexion"
      self.state = 0
      self.msg_index = 1
    elif self.state == 0:
      print "estado desconectado, en handshake"
      rx = self.getHandshakeMessageFor(msg)
      self.msg_index += 1
      self.sendMessage(rx)
    elif self.state == 1:
      print "estado conectado, respondiendo..."
      rx = self.getMessageFor(msg)
      self.sendMessage(rx)

  def sendMessage(self, msg):
    self.serial.write(msg)
    
  def read_serial(self, ser):
    rx = read_serial(ser)
    return rx
  
  def getNextFor(self,x):
    handshake_recieve = [
    #aaaa0000010000800a3131313131313131202003a7
    #aaaa0000010000800a50574e454421212120200400
    #aaaa00010100018340312020343630305a302e30335056203436303020202020202020202050484f454e495854454320202020202031313131313131312020202020202020343530300e28
    #aaaa00010100018340312020343630305a302e30335056203436303020202020202020202050484f454e495854454320202020202050574e45442121212020202020202020343530300e81
      ["aaaa0000010000800a50574e454421212120200400"],
      ["aaaa0000010000800a50574e454421212120200400"],
      ["aaaa000101000081010601de"],
      ["aaaa00010100018340312020343630305a302e30335056203436303020202020202020202050484f454e495854454320202020202050574e45442121212020202020202020343530300e81"],
      ["aaaa0001010001801b000102030405060d4041424344454748494a4c78797a7b7c7d7e7f08ed"],
      ["aaaa000101000181064041444546470375"],
      ["aaaa0001010001840c05dc001407a809e2132413ec05ac"]
    ]
    i = 0
    if x == "[aa][aa][1][0][0][0][0][0][0][1][55]":
        i = 1
        #[aa][aa][1][0][0][0][0][1][b][50][57][4e][45][44][21][21][21][20][20][1][3][83]
        #aaaa0100000000010b50574e4544212121202001 -> 383
    elif x == "[aa][aa][1][0][0][0][0][1][b][50][57][4e][45][44][21][21][21][20][20][1][3][83]":
        i = 2
    elif x == "[aa][aa][1][0][0][1][1][3][0][1][5a]":
        i = 3
    elif x == "[aa][aa][1][0][0][1][1][0][0][1][57]":
        i = 4
    elif x == "[aa][aa][1][0][0][1][1][1][0][1][58]":
        i = 5
    elif x == "[aa][aa][1][0][0][1][1][4][0][1][5b]":
        i = 6
        self.handshake_finished = True
    print "i es : ",i
    return handshake_recieve[i][0]
    
  def getDataNextFor(self,x):
    data_recieve = [
      ["aaaa0001010001823601ab00000aa40a9b0000003c003c03ab00000095083313900c7300000001b2c40000193b00010000000000000000000000000000000008f2"]
    ]
    i = 0
    if x == "[aa][aa][1][0][0][1][1][2][0][1][59]":
		return data_recieve[i][0]

  def work_forever(self):
    """
    q = "aaaa0000010000800a3131313131313131202003a7"
    #d = b'\x0F'
    #d = "ff"
    #print d
    hex_data = q.decode("hex")
    print hex_data
    #x = map(ord, hex_data)
    #print x
    self.serial.write(bytearray(q.decode("hex")))
    """
#    q = "aaaa0000010000800a3131313131313131202003a7"
    termino = False
    while True:
      print "entro al while"
      rx = self.read_serial(self.serial)
      print "lectura completa: "+rx
      lineOrd = ""
      lineHex = ""
      for byte in rx:
#        lineOrd += "["+str(ord(byte))+"]"
        lineHex += "["+str(hex(ord(byte))[2:])+"]"
#      print "RX as Ordinal:"
#      print lineOrd
      print "RX as Hexadecimal:"
      print lineHex
      #self.processMessage(rx)
      sig = self.getNextFor(lineHex)
      print self.handshake_finished
      print termino
      if not termino:
        lineHex = ""
        for byte in sig:
          lineHex += "["+str(hex(ord(byte))[2:])+"]"
        print "RESPONSE:"
        print lineHex
        self.serial.write(bytearray(sig.decode("hex")))
      if self.handshake_finished:
        termino = True
        r = self.getDataNextFor(lineHex)
        if r:
			self.serial.write(bytearray(r.decode("hex")))
        
      #time.sleep(1)


inversor = InversorSimulator()

inversor.iniciarlizar( "/dev/ttyS0" , 9600, 0.1 )

inversor.work_forever()


