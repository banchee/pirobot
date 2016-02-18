import sys
import time
from thread import *
import tank
import RPi.GPIO as GPIO
import tankcomms

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

def doubleMotorTankEngine(conn,tinyTim):
  count = 0
  while True:
    try:
      data = conn.recv(48).strip()
    except error, msg:
      print 'Data Received Failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    if not data:
      if count > 3:
        break
      count += 1

    coordinates = data.split(',')

    if len(coordinates) > 1:
      xpos = round((float(coordinates[0].split(':')[1].strip())* -1),1)
      ypos = round((float(coordinates[1].split(':')[1].strip())* -1),1)

      # print 'Y:' + str(ypos) + '\nX:' + str(xpos)

      if xpos > 3:
        tinyTim.left()
      elif xpos < -3:
        tinyTim.right()
      elif ypos > 3:
        tinyTim.forward()
      elif ypos < -3:
        tinyTim.reverse()
      else:
        tinyTim.stop()

      conn.sendall('')

  conn.close()

comms = tankcomms.tankcomms(8876)
comms.openSocket()
comms.sock.listen(1)
comms.sock.settimeout(10)

tinyTim = tank.tank()

GPIO.setup(tinyTim.right_motor.switchmodule.ch1, GPIO.OUT)
GPIO.setup(tinyTim.right_motor.switchmodule.ch2, GPIO.OUT)
GPIO.output(tinyTim.right_motor.switchmodule.ch1, 0)
GPIO.output(tinyTim.right_motor.switchmodule.ch2, 1)

GPIO.setup(tinyTim.left_motor.switchmodule.ch1, GPIO.OUT)
GPIO.setup(tinyTim.left_motor.switchmodule.ch2, GPIO.OUT)
GPIO.output(tinyTim.left_motor.switchmodule.ch1, 0)
GPIO.output(tinyTim.left_motor.switchmodule.ch2, 1)


while 1:
  try:
    conn, addr = comms.sock.accept()
    start_new_thread(doubleMotorTankEngine, (conn,tinyTim))
  except:
    print 'error'
    break

comms.sock.close()
GPIO.cleanup()
print 'Connection closed'



