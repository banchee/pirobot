import switch

class motor(object):

  def __init__(self, ch1=0, ch2=0):
    self.switch = switch.switch(0, ch1, ch2)

  def positive(self):
    self.switch.on()

  def negative(self):
    self.switch.off()

  def stop(self):
    self.switch.idle()
