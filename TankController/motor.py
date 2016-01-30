import switch

class motor(object):

  def __init__(self, ch1=0, ch2=0):
    self.switchmodule = switch.switch(0, ch1, ch2)

  def positive(self):
    self.switchmodule.on()

  def negative(self):
    self.switchmodule.off()

  def stop(self):
    self.switchmodule.idle()
