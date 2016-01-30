import RPi.GPIO as gpio

GPIO.setmode(GPIO.BOARD)

class switch(object):
  def __init__(self, vccpin=0, ch1=0, ch2=0):
    self.vccpin = vccpin
    self.ch1 = ch1
    self.ch2 = ch2

    self.gpioSetup

  def gpioSetup(self):
    gpio.setup(self.vccpin, gpio.OUT)
    gpio.setup(self.ch1, gpio.OUT)
    gpio.setup(self.ch2, gpio.OUT)
    gpio.output(self.vccpin, 0)
    gpio.output(self.ch1, 0)
    gpio.output(self.ch2, 0)

  def powerSwitch(self, off_on=0):
    gpio.output(self.vccpin, off_on)

  def on(self):
    gpio.output(self.ch1, 1)
    gpio.output(self.ch1, 1)

  def off(self):
    gpio.output(self.ch1, 0)
    gpio.output(self.ch1, 0)

  def idle(self):
    gpio.output(self.ch1, 0)
    gpio.output(self.ch1, 1)
