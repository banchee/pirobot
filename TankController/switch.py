import RPi.GPIO as gpio

class Switch(object):
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

  def channelOn(channel=0):
    if channel == 1:
      gpio.output(self.ch1, 1)
    elif channel > 1:
      gpio.output(self.ch2, 1)

  def channelOff(channel=0):
    if channel == 1:
      gpio.output(self.ch1, 0)
    elif channel > 1:
      gpio.output(self.ch2, 0)

  def on(self):
    self.channelOn(1)
    self.channelOn(2)

  def off(self):
    self.channelOff(1)
    self.channelOff(2)

  def idle(self):
    self.channelOn(1)
    self.channelOff(2)