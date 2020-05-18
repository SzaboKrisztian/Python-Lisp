import collections, global_env, lisp_types

class Environment():
  """
  Environment represents an associative data structure that holds Symbols (or Keywords) and some associated value. Internally it uses a Python dictionary to achieve this. Environments can also be nested within each other (thus enabling scoping) by the way of the 'outer' attribute
  """
  def __init__(self, outer=None, keys=(), vals=(), is_global=False):
    self.outer = outer
    self.data = dict()
    if is_global:
      # If the global environment is supposed to be instantiated, then we want to load all the basic functions
      self.data.update(global_env.funcs)
    # If any key/values are provided, they are to be paired up and added to the environment being created
    for i in range(len(keys)):
      if keys[i] == "&":
        # If the "&" symbol is encountered in the keys list, then all the remaining values not yet processed, will be bound as a list to the symbol following after "&"
        self.data[keys[i + 1]] = lisp_types.List(vals[i:])
        break
      else:
        self.data[keys[i]] = vals[i]

  def define(self, key, value):
    """ Create a new association in the current environment. """
    self.data[key] = value

  def get(self, key):
    """ Retrieves the value associated with a key, or throws an exception if it doesn't exist. """
    env = self.find(key)
    if env is None:
      raise ValueError(f"{key} not found")
    else:
      return env[key]

  def find(self, key):
    """ Recursive function that searches for a key starting in the current environment, and working its way to the outermost one. It will return the environment in which the key is found, or None if it's not found. """
    if key in self.data:
      return self.data
    elif self.outer is not None:
      return self.outer.find(key)
    else:
      return None