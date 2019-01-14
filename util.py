""" Utiliy stuff """

class IdGenerator:
  """ Class ussed to generate non repeated ids and keep track of the current ones """

  def __init__(self):
    self.last_id = 0
    self.used = set()

  def next_id(self):
    self.last_id += 1
    self.used.add(last_id)
    return self.last_id

  def destroy_id(self, tid):
    if tid not in used:
      raise ValueError('')
