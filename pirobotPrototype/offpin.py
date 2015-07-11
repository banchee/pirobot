import RPi.GPIO as GPIO
import time
import motordrive 

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

m = motordrive.motorDriver(7,11,13,12)

m.start()

m.forward()

time.sleep(3)

m.reverse()

time.sleep(3)

m.stop()




