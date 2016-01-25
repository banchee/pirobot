import motor

class tank(object):
  def __init__(self):
    self.left_motor  = motor.motor(11,15)
    self.right_motor = motor.motor(11,15)
    self.actions = {'forward':False, 'reverse':False, 'left':False, 'right':False, 'stop':True}

  def forward(self):
    if not self.actions['forward']:
      self.left_motor.positive()
      self.right_motor.positive()

      for key, value in self.actions.items():
        if key == 'forward':
          self.actions[key] = True
        else:
          self.actions[key] = False

  def reverse(self):
    if not self.actions['reverse']:
      self.left_motor.negative()
      self.right_motor.negative()

      for key, value in self.actions.items():
          if key == 'reverse':
            self.actions[key] = True
          else:
            self.actions[key] = False

  def left(self):
    if not self.actions['left']:
      self.left_motor.positive()
      self.right_motor.negative()

      for key, value in self.actions.items():
          if key == 'left':
            self.actions[key] = True
          else:
            self.actions[key] = False

  def right(self):
    if not self.actions['right']:
      self.left_motor.negative()
      self.right_motor.positive()

      for key, value in self.actions.items():
          if key == 'right':
            self.actions[key] = True
          else:
            self.actions[key] = False

  def stop(self):
    if not self.actions['stop']:
      self.left_motor.stop()
      self.left_motor.stop()

      for key, value in self.actions.items():
          if key == 'static':
            self.actions[key] = True
          else:
            self.actions[key] = False
