import socket
import sys
from thread import *
import RPi.GPIO as GPIO
import time
import motordrive

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#Functions and stuff
#------------------------------------------------------------------
def newThread(conn, MotorDrive):

    lForward = False
    lReverse = False

    while True:
        try:
            data  = conn.recv(1024).strip()
        except error, msg:
            print 'Data Received Failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        if not data :
            break

        co_ordinates = data.split(',')

        cx = co_ordinates[0].split(':')
        cy = co_ordinates[1].split(':')
        cx = ''.join(cx[1])
        cy = ''.join(cy[1])
        cx = cx.strip()
        cy = cy.strip()

        x = float(cx)
        y = float(cy)

        print 'Y:' + str(y) + '\nX:' + str(x)

        if y > 2:
            if not lReverse:
                MotorDrive.reverse()
                lReverse = True
                lForward = False
        if  y < -2:
            if not lForward:
                MotorDrive.forward()
                lReverse = False
                lForward = True

        conn.sendall('')

    conn.close()
    MotorDrive.stop ()

#-----------------------------------------------------------

MotorA = motordrive.motorDriver(7,11,15,12)

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8875 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
s.settimeout(10)

try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    #sys.exit()

print 'Socket bind complete'

s.listen(1)
print 'Socket now listening'

while 1:
    try:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        #display client information
        start_new_thread(newThread, (conn,MotorA))
    except socket.error , msg:
        break


s.close()

GPIO.cleanup()

