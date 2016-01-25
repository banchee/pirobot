import sys
import time
from thread import *
import tank
import RPi.GPIO as GPIO
import tankcomms

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

def doubleMotorTankEngine(conn):
  tank = tank.tank()
  count = 0
  while True:
    try:
      data = conn.recv(100).strip()
    except error, msg:
      print 'Data Received Failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    if not data:
      if count > 3:
        break
      count += 1

    coordinates = data.split(',')
    xpos = (float(coordinates[0].split(':')[1].strip()) * -1)
    ypos = (float(coordinates[1].split(':')[1].strip()) * -1)

    print 'Y:' + str(ypos) + '\nX:' + str(xpos)

    if (ypos > 2 or yos < -2) and xpos > 2
      tank.right()
    elif (ypos > 2 or ypos < -2) and xpos < -2
      tank.left()
    elif ypos > 2
      tank.forward()
    elif ypos < -2
      tank.reverse()
    elif xpos > 2
      tank.left()
    elif xpos < -2
      tank.right()
    else
      tank.stop()

    conn.sendall('')

  tank.stop()
  conn.close()

comms = comms.comms(8875)
comms.openSocket()
comms.socket.listen(1)

while 1:
  try:
    conn, addr comms.socket.accept()
    start_new_thread(doubleMotorTankEngine, conn)
  except comms.socket.error, msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    break


comms.close()
GPIO.cleanup()




