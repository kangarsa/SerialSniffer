# coding=utf-8
import serial
import time
import binascii
import random
import pprint
import dataParser

#from pymongo import MongoClient
#from bson.objectid import ObjectId


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
  return int(bytes, 16)


#def checksum(bytes):
#    suma = 0
#    for b in bytes:
#        suma += ord(b)
#    return suma

def checksum(b):
  suma = 0
  for x in range(0,len(b),2):
    suma += bytes_to_int(b[x:x+2])
  return suma

class InversorSimulator () :
  state = 0
  msg_index = 0
  port = "/dev/ttyS0"
  baud_rate = 9600
  timeout = 0.1
  handshake_finished = False
  
  secNumber = 910
  incrementSecNumber = 1

  lastEnergyToday = 0
  incrementET = 1
  
  lastEnergyTotal = 10532
  incrementETotal = 1

  lastIAC = 50.0
  varIAC = 0.0
  minIAC = 10.0
  maxIAC = 100.0

  lastPAC = 1100
  varPAC = 0
  minPAC = 200
  maxPAC = 4500
  
  varPercentLast = 0.01
  varPercentMax = 0.2

  read_index = 0
  
  tmp_i = 1

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
    
  # int getLastEnergyTotal():
  def getETotal(self):
    self.lastEnergyTotal += self.incrementETotal
    return self.lastEnergyTotal
    
  # int getSecNumber():
  def getSecNumber(self):
    self.secNumber += self.incrementSecNumber
    return self.secNumber
    
  def randomChange(self):
    self.varPercentLast = random.uniform(-self.varPercentMax,self.varPercentMax)
    print "RAND:: ", self.varPercentLast
    #if aux < self.varPercentMax and aux > self.varPercentMax:
    #  self.varPercentLast = aux
    return self.varPercentLast

  # float getIAC():
  def getIAC(self):
    #aux = self.lastIAC+random.uniform(-self.varIAC,self.varIAC)
    aux = self.lastIAC+(self.lastIAC*self.varPercentLast)
    if aux < self.maxIAC and aux > self.minIAC:
      self.lastIAC = aux
    print "IAC: ",self.lastIAC
    return self.lastIAC

  # int getPAC(int, int):
  def getPAC(self):
    #aux = self.lastPAC = self.lastPAC+random.randint(-self.varPAC,self.varPAC)
    aux = int(self.lastPAC+(self.lastPAC*self.varPercentLast))
    if aux < self.maxPAC and aux > self.minPAC:
      self.lastPAC = aux
    print "PAC: ",self.lastPAC
    return self.lastPAC

  # string(hex) getHexIAC():
  def getHexSN(self):
    return hex(int(self.getSecNumber()))[2:]
    
  # string(hex) getHexET():
  def getHexET(self):
    return hex(int(self.getET()))[2:]
    
  # string(hex) getHexETotal():
  def getHexETotal(self):
    return hex(int(self.getETotal()))[2:]

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
    self.randomChange()
    base = list("01ab00000aa40a9b0000003c003c03ab00000095083313900c7300000001b2c40000193b000100000000000000000000000000000000")
    et = self.completeHexWith(4,self.getHexET())
    base[28] = et[0]
    base[29] = et[1]
    base[30] = et[2]
    base[31] = et[3]
    iac = self.completeHexWith(4,self.getHexIAC())
    base[36] = iac[0]
    base[37] = iac[1]
    base[38] = iac[2]
    base[39] = iac[3]
    pac = self.completeHexWith(4,self.getHexPAC())
    base[48] = pac[0]
    base[49] = pac[1]
    base[50] = pac[2]
    base[51] = pac[3]
    etotal = self.completeHexWith(8,self.getHexETotal())
    base[56] = etotal[0]
    base[57] = etotal[1]
    base[58] = etotal[2]
    base[59] = etotal[3]
    base[60] = etotal[4]
    base[61] = etotal[5]
    base[62] = etotal[6]
    base[63] = etotal[7]
    return "".join(base)

  def getDataNextFor(self,x):
    i = 0
    if x == "[aa][aa][1][0][0][1][1][2][0][1][59]":
      header_body = self.getNewHeader()+self.getNewBody()
      #print header_body
      cs = self.completeHexWith(4,hex(checksum(header_body))[2:])
      #print cs
      hdf = header_body+cs
      data_recieve = [
        [hdf],
        ["aaaa0001010001823601ab00000aa40a9b0000003c003c03ab00000095083313900c7300000001b2c40000193b00010000000000000000000000000000000008f2"],
        ["aaaa00010100018236019d00000ad00ae20000001b001b038c000000430850139105b600000001b2c10000193b00010000000000000000000000000000000080fb"],
        ["aaaa00010100018236019d00000a1709ec0000001d001d038c000000440850139105af00000001b2c10000193b0001000000000000000000000000000000000849"],
        ["aaaa00010100018236019d000008e408c1000000250025038c0000004808471390065500000001b2c10000193b0001000000000000000000000000000000000899"],
        ["aaaa00010100018236019c0000094d0919000000280029038d0000005308471391074000000001b2c20000193b000100000000000000000000000000000000075c"],
        ["aaaa00010100018236019a00000a8a0a3b0000002a002b038d0000006708501392089300000001b2c20000193b0001000000000000000000000000000000000831"],
        ["aaaa00010100018236019a00000a8a0a3b0000002a002b038d0000006708501392089300000001b2c20000193b0001000000000000000000000000000000000831"],
        ["aaaa00010100018236019a00000a8a0a3b0000002a002b038d0000006708501392089300000001b2c20000193b0001000000000000000000000000000000000831"],
        ["aaaa00010100018236019a00000a8a0a3b0000002a002b038e0000006708501392089300000001b2c20000193b0001000000000000000000000000000000000832"],
        ["aaaa00010100018236019a00000a8a0a3b0000002a002b038e0000006708501392089300000001b2c20000193b0001000000000000000000000000000000000832"],
        ["aaaa00010100018236019a00000a8a0a3b0000002a002b038e0000006708501392089300000001b2c20000193b0001000000000000000000000000000000000832"],
        ["aaaa00010100018236019a00000a8a0a3b0000002a002b038f0000006708501392089300000001b2c20000193b0001000000000000000000000000000000000833"],
        ["aaaa00010100018236019a00000a8a0a3b0000002a002b038f0000006708501392089300000001b2c20000193b0001000000000000000000000000000000000833"],
        ["aaaa00010100018236019a00000a8a0a3b0000002a002b038f0000006708501392089300000001b2c20000193b0001000000000000000000000000000000000833"],
        ["aaaa00010100018236019a00000a8a0a3b0000002a002b038f0000006708501392089300000001b2c20000193b0001000000000000000000000000000000000833"],
        ["aaaa00010100018236019a00000a8a0a3b0000002a002b038f0000006708501392089300000001b2c20000193b0001000000000000000000000000000000000833"],
        ["aaaa00010100018236019a00000a8a0a3b0000002a002b038f0000006708501392089300000001b2c20000193b0001000000000000000000000000000000000833"],
        ["aaaa00010100018236019a00000a8a0a3b0000002a002b038f0000006708501392089300000001b2c20000193b0001000000000000000000000000000000000833"],
        ["aaaa00010100018236019a00000a8a0a3b0000002a002b038f0000006708501392089300000001b2c20000193b0001000000000000000000000000000000000833"],
        ["aaaa00010100018236019a00000a8a0a3b0000002a002b038f0000006708501392089300000001b2c20000193b0001000000000000000000000000000000000833"],
        ["aaaa00010100018236019a00000a8a0a3b0000002a002b038f0000006708501392089300000001b2c20000193b0001000000000000000000000000000000000833"],
        ["aaaa00010100018236019a00000a8a0a3b0000002a002b038f0000006708501392089300000001b2c20000193b0001000000000000000000000000000000000833"]
      ]
      # data_recieve siendo usado:
      self.tmp_i += 1
      print "arreglo i:",self.tmp_i
      return data_recieve[i][0]
      #return data_recieve[self.tmp_i][0]

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
      rx = self.read_serial(self.serial)
      #rx = self.simulateReadSerial()
      print "lectura completa: "+rx
      lineOrd = ""
      lineHex = ""
      crudo = ""
      for byte in rx:
        #Print SERIAL READ
        c = str(hex(ord(byte))[2:])
        #lineHex += "["+str(hex(ord(byte))[2:])+"]"
        #print lineHex
        #Print SIMULATED
        #c = str(hex(byte)[2:])
        crudo += c
        lineHex += "["+c+"]"
        pass
      #print "RX as Ordinal:"
      #print lineOrd


      print "RX as Hexadecimal:"
      print lineHex
      #self.processMessage(rx)
      if not self.handshake_finished:
        sig = self.getNextFor(lineHex)
      else:
        sig = self.getDataNextFor(lineHex)
      #f = open("last_data_raw","w")
      #f.write(sig)
      #f.close()
      print "handshake_finished: "+str(self.handshake_finished)
      lineHex = ""
      #pp = pprint.PrettyPrinter(indent=2)
      #print "SIG",sig
      #print "PARSED: "
      #pp.pprint(dataParser.generateJson(sig))
      if sig:
        #for byte in sig:
        #  lineHex += "["+str(hex(ord(byte))[2:])+"]"
      
        for i in range(0,len(sig)-1,2):
          lineHex += "["+sig[i:i+2]+"]"
        print "RESPONSE:"
        print lineHex
        #SALIDA:
        self.serial.write(bytearray(sig.decode("hex")))

      #client = MongoClient('mongodb://localhost:27017/')
      #db = client.serial_database
      #oi = ObjectId()
      #print oi
      #db.reads.update(
      #        { "_id": oi },
      #        { "data": sig },
      #        upsert=True
      #    )
        
      #time.sleep(1)


inversor = InversorSimulator()

#inversor.iniciarlizar( "/dev/pts/0" , 9600, 0.1 )
inversor.iniciarlizar( "/dev/ttyS0" , 9600, 0.05 )

inversor.work_forever()

