import sys
import time
from thread import *
import tank
import RPi.GPIO as GPIO
import tankcomms

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

def doubleMotorTankEngine(conn):
  tinyTim = tank.tank()
  count = 0
  while True:
    try:
      data = conn.recv(1024).strip()
    except error, msg:
      print 'Data Received Failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    if not data:
      if count > 3:
        break
      count += 1

    coordinates = data.split(',')
    if len(coordinates) > 1:
      xpos = round((float(coordinates[0].split(':')[1].strip()) * -1),1)
      ypos = round((float(coordinates[1].split(':')[1].strip()) * -1),1)

    print 'Y:' + str(ypos) + '\nX:' + str(xpos)

    if (ypos > 2 or ypos < -2) and xpos > 2:
      tinyTim.right()
    elif (ypos > 2 or ypos < -2) and xpos < -2:
      tinyTim.left()
    elif ypos > 2:
      tinyTim.forward()
    elif ypos < -2:
      tinyTim.reverse()
    elif xpos > 2:
      tinyTim.left()
    elif xpos < -2:
      tinyTim.right()
    else:
      tinyTim.stop()

    conn.sendall('')

  tinyTim.stop()
  conn.close()

comms = tankcomms.tankcomms(8875)
comms.openSocket()
comms.sock.listen(1)
comms.sock.settimeout(10)

while 1:
  try:
    conn, addr = comms.sock.accept()
    start_new_thread(doubleMotorTankEngine, (conn,))
  except error, msg:
    break

comms.close()
GPIO.cleanup()
print 'Connection closed'



