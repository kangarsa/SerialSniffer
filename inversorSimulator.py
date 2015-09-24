# coding=utf-8
import serial
import time
import binascii
import random


def read_serial(ser):
  buf = ''
  while True:
    inp = ser.read(500) #read 500 bytes or do timeout
    buf = buf + inp #accumalate the response
    if buf != '':
      return buf

def int_to_bytes(i): #transforma a hexadecimal cadenas de largas, para 1 byte usar ord(byte)
  return format(i, 'x')

def bytes_to_int(bytes): #transforma a hexadecimal cadenas de largas, para 1 byte usar ord(byte)
  return int(bytes.encode('hex'), 16)


def checksum(bytes):
    suma = 0
    for b in bytes:
        suma += ord(b)
    return suma

class InversorSimulator () :
  state = 0
  msg_index = 0
  port = "/dev/ttyS0"
  baud_rate = 9600
  timeout = 0.1
  handshake_finished = False

  lastEnergyToday = 0
  incrementET = 1

  lastIAC = 5.0
  varIAC = 1.0
  minIAC = 0.0
  maxIAC = 10.0

  lastPAC = 500
  varPAC = 2
  minPAC = 0
  maxPAC = 1000

  read_index = 0

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


  handshake_send = [
  ["59aa010000000000000155"],
  ["aaaa0100000000010b3131313131313131202001032a"],
  ["aaaa01000001010300015a"],
  ["aaaa010000010100000157"],
  ["aaaa010000010101000158"],
  ["aaaa01000001010400015b"]
  ]

  def iniciarlizar(self, port, baud_rate, timeout):
    print "iniciando inversor..."
    self.port = port
    self.baud_rate = baud_rate
    self.timeout = timeout
    state = 0
    #self.serial = serial.Serial(port=port,baudrate=baud_rate,timeout=timeout)
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
    # Original: aaaa0000010000800a3131313131313131202003a7
    # PWNED: aaaa0000010000800a50574e454421212120200400
    # Original: aaaa00010100018340312020343630305a302e30335056203436303020202020202020202050484f454e495854454320202020202031313131313131312020202020202020343530300e28
    # PWNED: aaaa00010100018340312020343630305a302e30335056203436303020202020202020202050484f454e495854454320202020202050574e45442121212020202020202020343530300e81
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
        # Original: [aa][aa][0][0][1][0][0][80][a][31][31][31][31][31][31][31][31][20][20][3][a7]
        # PWNED: [aa][aa][1][0][0][0][0][1][b][50][57][4e][45][44][21][21][21][20][20][1][3][83]
        # aaaa0100000000010b50574e4544212121202001 -> 383
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

  # int getLastEnergyToday():
  def getET(self):
    self.lastEnergyToday += self.incrementET
    return self.lastEnergyToday

  # float getIAC():
  def getIAC(self):
    aux = self.lastIAC+random.uniform(-self.varIAC,self.varIAC)
    if aux < self.maxIAC and aux > self.minIAC:
      self.lastIAC = aux
    return self.lastIAC

  # int getPAC(int, int):
  def getPAC(self):
    aux = self.lastPAC = self.lastPAC+random.randint(-self.varPAC,self.varPAC)
    if aux < self.maxPAC and aux > self.minPAC:
      self.lastPAC = aux
    return self.lastPAC

  # string(hex) getHexIAC():
  def getHexET(self):
    return hex(int(self.getET()))[2:]

  # string(hex) getHexIAC():
  def getHexIAC(self):
    return hex(int(self.getIAC()))[2:]

  # string(hex) getHexIAC():
  def getHexPAC(self):
    return format(int(self.getPAC()), 'x')

  def getChecksum(self,data):
    return format(checksum(data), 'x')

  def completeHexWith(self,length,h):
    r = ""
    for x in range(0,length-len(h)):
      r += "0"
    return r + h

  def getNewHeader(self):
    return "aaaa00010100018236"

  def getNewBody(self):
    # plantear strategy aca!
    base = list("01ab00000aa40a9b0000003c003c03ab00000095083313900c7300000001b2c40000193b000100000000000000000000000000000000")
    et = self.completeHexWith(4,self.getHexET())
    base[28] = et[0]
    base[29] = et[1]
    base[30] = et[2]
    base[31] = et[3]
    iac = self.completeHexWith(4,self.getHexIAC())
    base[38] = iac[0]
    base[39] = iac[1]
    base[40] = iac[2]
    base[41] = iac[3]
    pac = self.completeHexWith(4,self.getHexPAC())
    base[50] = pac[0]
    base[51] = pac[1]
    base[52] = pac[2]
    base[53] = pac[3]
    return "".join(base)

  def getDataNextFor(self,x):
    header_body = self.getNewHeader()+self.getNewBody()
    hdf = header_body+hex(checksum(header_body))[2:]
    data_recieve = [
      [hdf],
      ["aaaa0001010001823601ab00000aa40a9b0000003c003c03ab00000095083313900c7300000001b2c40000193b00010000000000000000000000000000000008f2"]
    ]
    # data_recieve siendo usado:
    i = 0
    if x == "[aa][aa][1][0][0][1][1][2][0][1][59]":
		  return data_recieve[i][0]

  def simulateReadSerial(self):
    value = ""
    if not self.handshake_finished:
      value = self.handshake_send[self.read_index][0]
      if self.read_index < len(self.handshake_send)-1:
        self.read_index += 1
    else:
      value = "aaaa010000010102000159"
    return self.string_to_byte_array(value)


  def string_to_byte_array(self, s):
    """
    r = 
    for x in range(0,len(s)-1,2):
      v = s[x]+s[x+1]
      print "data: "+v
      hex_data = hex_string.decode("hex")
    """
    hex_string = s
    hex_data = hex_string.decode("hex")
    return bytearray(hex_data)

  def int_to_bytes(self,i):
    return int_to_bytes(i)

  def bytes_to_int(self, b):
    return bytes_to_int(b)

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
      # ENTRADA:
      #rx = self.read_serial(self.serial)
      rx = self.simulateReadSerial()
      print "lectura completa: "+rx
      lineOrd = ""
      lineHex = ""
      for byte in rx:
        #lineHex += "["+str(hex(ord(byte))[2:])+"]"
        lineHex += "["+str(hex(byte)[2:])+"]"
#      print "RX as Ordinal:"
#      print lineOrd
      print "RX as Hexadecimal:"
      print lineHex
      #self.processMessage(rx)
      if not self.handshake_finished:
        sig = self.getNextFor(lineHex)
      else:
        sig = self.getDataNextFor(lineHex)

      print "handshake_finished: "+str(self.handshake_finished)
      lineHex = ""
      print sig
      """for byte in sig:
                          lineHex += "["+str(hex(ord(byte))[2:])+"]" """
      for i in range(0,len(sig)-1,2):
        lineHex += "["+sig[i:i+2]+"]"
      print "RESPONSE:"
      print lineHex
      #SALIDA:
      #self.serial.write(bytearray(sig.decode("hex")))
      #####self.serial.write(self.string_to_byte_array(r))????
      if sig:
        #self.serial.write(bytearray(r.decode("hex")))
        print sig
        
      time.sleep(1)


inversor = InversorSimulator()

inversor.iniciarlizar( "/dev/ttyS0" , 9600, 0.1 )

inversor.work_forever()


