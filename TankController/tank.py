import motor

class tank(object):
  def __init__(self):
    self.left_motor  = motor.motor(7,11)
    self.right_motor = motor.motor(12,13)
    self.actions = {'forward':False, 'reverse':False, 'left':False, 'right':False, 'stop':False}

  def forward(self):
    if not self.actions['forward']:
      print 'Forward'
      self.left_motor.positive()
      self.right_motor.positive()

      for key, value in self.actions.items():
        if key == 'forward':
          self.actions[key] = True
        else:
          self.actions[key] = False

  def reverse(self):
    if not self.actions['reverse']:
      print 'Reverse'
      self.left_motor.negative()
      self.right_motor.negative()

      for key, value in self.actions.items():
          if key == 'reverse':
            self.actions[key] = True
          else:
            self.actions[key] = False

  def left(self):
    if not self.actions['left']:
      print 'Left'
      self.left_motor.positive()
      self.right_motor.negative()

      for key, value in self.actions.items():
          if key == 'left':
            self.actions[key] = True
          else:
            self.actions[key] = False

  def right(self):
    if not self.actions['right']:
      print 'Right'
      self.left_motor.negative()
      self.right_motor.positive()

      for key, value in self.actions.items():
          if key == 'right':
            self.actions[key] = True
          else:
            self.actions[key] = False

  def stop(self):
    if not self.actions['stop']:
      print 'Idle'
      self.left_motor.stop()
      self.right_motor.stop()

      for key, value in self.actions.items():
          if key == 'stop':
            self.actions[key] = True
          else:
            self.actions[key] = False
