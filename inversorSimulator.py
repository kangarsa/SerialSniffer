import serial
import time

class InversorSimulator () :
  state = 0
  msg_index = 0
  port = "/dev/pts/12"
  baud_rate = 9600
  timeout = 0.1

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

  #method for reading incoming bytes on serial
  def read_serial(self, ser):
    buf = ''
    while True:
      inp = ser.read(1) #read 1 bytes or do timeout
      buf = buf + inp #accumalate the response
      print "-------"+buf
      print len(buf)
      print self.handshake_monitor[self.msg_index]
      print len(self.handshake_monitor[self.msg_index])
      if len(buf) > 7:
        if buf[0:8] != "[aa][aa]":
          buf = ''
      if inp == '' or buf in self.monitor_messages:
        # recibe nada o llegó uno de los esperados
        return buf

  def work_forever(self):
    while True:
      rx = self.read_serial(self.serial)
      print "lectura completa: "+rx
      self.processMessage(rx)
      time.sleep(1)


inversor = InversorSimulator()

inversor.iniciarlizar( "/dev/pts/12" , 9600, 0.1 )

inversor.work_forever()


