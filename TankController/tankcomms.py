import socket

class tankcomms(object):

  def __init__(self, port=8875):
    self.HOST = ''
    self.PORT = port
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def openSocket(self):
    try:
      self.sock.bind((self.HOST, self.PORT))
    except socket.error , msg:
      print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]

  def closeSocket(self):
    self.socket.close()
