import RPi.GPIO as GPIO
class motorDriver(object):
    def __init__(self, powerpin=0, swpin1=0, swpin2=0, pwmpin=0):
        self.PowerPin  = powerpin
        self.SitchPins = [swpin1,swpin2]
        self.PwmPin    = pwmpin
        self.ON        = 0

        GPIO.setup(self.PowerPin    , GPIO.OUT)
        GPIO.setup(self.SitchPins[0], GPIO.OUT)
        GPIO.setup(self.SitchPins[1], GPIO.OUT)
        GPIO.setup(self.PwmPin      , GPIO.OUT)

        GPIO.output(self.PowerPin    , 0)
        GPIO.output(self.SitchPins[0], 0)
        GPIO.output(self.SitchPins[0], 0)
        GPIO.output(self.PwmPin      , 0)
        
    def forward(self):
        GPIO.output(self.SitchPins[0], 1)
        GPIO.output(self.SitchPins[1], 1)

    def reverse(self):
        GPIO.output(self.SitchPins[0], 0)
        GPIO.output(self.SitchPins[1], 0)

    def stop(self):
        GPIO.output(self.PowerPin   , 0)

    def start(self):
        GPIO.output(self.PowerPin   , 1)