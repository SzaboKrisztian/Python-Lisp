import collections, re

# Atomic types

class Symbol(collections.UserString):
  def __eq__(self, other):
    return isinstance(other, Symbol) and self.data == other.data
  def __hash__(self):
    return hash(self.data)

class Keyword(collections.UserString):
  pattern = re.compile(r':[a-zA-Z0-9\-*+!_\'?<>=]*')
  def __init__(self, value):
    if re.fullmatch(Keyword.pattern, value) is None:
      raise ValueError("Invalid keyword")
    super().__init__(value)

  def __eq__(self, other):
    if isinstance(other, Keyword):
      return self.data == other.data
    else:
      return False

  def __hash__(self):
    return hash(self.data)

class SForm(collections.UserString):
  pass

class Atom:
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return f"(atom {self.value})"

class Nil:
  def __repr__(self):
    return "nil"

  def __eq__(self, other):
    return isinstance(other, Nil)

  def __len__(self):
    return 0

# Collection types

class List(collections.UserList):
  pass

class Vector(collections.UserList):
  pass

class Map(collections.UserDict):
  pass

# Function type

class Procedure:
  def __init__(self, ast, params, env, fn, is_macro=False):
    self.ast = ast
    self.params = params
    self.env = env
    self.fn = fn
    self.make_env = lambda Env, args: Env(env, params, args)
    self.is_macro = is_macro
  
  def __call__(self, *args):
    return self.fn(*args)

# Exceptions

class BlankLine(Exception):
  pass

# Some helper functions

def parse_str(value):
    pattern = re.compile(r'"(?:[\\].|[^\\"])*"')
    if re.match(pattern, value):
      return unescape(value[1:-1])
    else:
      raise ValueError("Not a valid string")

def unescape(string):
  return string.replace('\\\\', '\u00b6').replace('\\n', '\n').replace('\\"', '"').replace('\u00b6', '\\')