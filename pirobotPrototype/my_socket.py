import socket
import sys
from thread import *
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

class LEd:
    def __init__(LEd, pinum=0, indicatorsensor=''):
        LEd.pinnum = pinum
        LEd.indicatorsensor = indicatorsensor
        LEd.indicatorsensorvalue = 0.0
        LEd.pulsepercent = 0.0
        LEd.powervalue = 0
        LEd.active = False 

        print 'Led int: ' + str(pinum) + ' indicator sensor: ' + indicatorsensor

    def setupLEd(LEd):
        GPIO.setup(LEd.pinnum, GPIO.OUT)
        LEd.Pwm = GPIO.PWM(LEd.pinnum,100)

    def changePwmPulse (LEd):
        Max = 300.0 
        Min = -300.0
        
            
        if '+' in LEd.indicatorsensor:
            if Max > LEd.indicatorsensorvalue >= 40.0 :
                LEd.pulsepercent = round((LEd.indicatorsensorvalue / Max) * 100, 0)
            else:
                LEd.pulsepercent = 0
        elif '-' in LEd.indicatorsensor:
            if Min < LEd.indicatorsensorvalue <= -40.0 :
                LEd.pulsepercent = round((LEd.indicatorsensorvalue / Min) * 100, 0)
            else:
                LEd.pulsepercent = 0
        
    def updateLEdSensorValue (LEd, x = 0.0 , y = 0.0):
        if 'x' in LEd.indicatorsensor:
            LEd.indicatorsensorvalue = (x * 30)
        elif 'y' in LEd.indicatorsensor:
            LEd.indicatorsensorvalue = (y * 30) 

    def commit(LEd):
        if LEd.active: 
            LEd.update()
        print str(LEd.indicatorsensor) + ' - Pulse %:' + str(LEd.pulsepercent) + ' Sensor Value:' + str(LEd.indicatorsensorvalue)

    def update (LEd):
        LEd.changePwmPulse()
        LEd.Pwm.ChangeDutyCycle(int(round(LEd.pulsepercent,0)))

def newThread(conn):
    LedList = [ledYPos,ledYNeg,ledXPos,ledXNeg]
    while True:
        try: 
            data  = conn.recv(1024).strip()
        except error, msg: 
            print 'Data Received Failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        if not data :
            break
        ledYPos.active = True
        ledYNeg.active = True
        ledXPos.active = True
        ledXNeg.active = True

        co_ordinates = data.split(',')
        
        cx = co_ordinates[0].split(':') 
        cy = co_ordinates[1].split(':')
        cx = ''.join(cx[1])
        cy = ''.join(cy[1])
        cx = cx.strip()
        cy = cy.strip()

        x = float(cx)     
        y = float(cy)
        
        ledYPos.updateLEdSensorValue(x , y)
        ledYNeg.updateLEdSensorValue(x , y)
        ledXPos.updateLEdSensorValue(x , y)
        ledXNeg.updateLEdSensorValue(x , y)

        ledYPos.commit()
        ledYNeg.commit()
        ledXPos.commit()
        ledXNeg.commit()

        conn.sendall('')
        
    conn.close()
    ledYPos.active = False
    ledYNeg.active = False
    ledXPos.active = False
    ledXNeg.active = False

    
GPIO.setwarnings(False)

ledYPos = LEd(7,'y(+)')
ledYNeg = LEd(11,'y(-)')
ledXPos = LEd(15,'x(+)')
ledXNeg = LEd(13,'x(-)')

ledYPos.setupLEd()
ledYNeg.setupLEd()
ledXPos.setupLEd()
ledXNeg.setupLEd()

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8874 # Arbitrary non-privileged port

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

ledYPos.Pwm.start(0)
ledYNeg.Pwm.start(0)
ledXPos.Pwm.start(0)
ledXNeg.Pwm.start(0)

while 1:
    try:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        #display client information
        start_new_thread(newThread, (conn,))
    except socket.error , msg:
        break 
    

s.close()

ledYPos.Pwm.stop()
ledYNeg.Pwm.stop()
ledXPos.Pwm.stop()
ledXNeg.Pwm.stop()

GPIO.cleanup() 

