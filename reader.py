import re
from lisp_types import *

# Magic regex that breaks a string apart in tokens, according to the language's syntax
token_pattern = re.compile(r'(?=.)[\s,]*(~@|[\[\]{}()\'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}(\'"`,;)]*)')

# Some values that are treated in special ways
unique_values = {"nil": Nil(), "true": True, "false": False, "&": SForm("&")}

class Reader:
  """ Internally holds a sequence of tokens and a cursor that points to one of them """
  def __init__(self, tokens):
    self.position = 0
    self.tokens = tokens

  def next(self):
    """ Return the current token, and move the cursor to the next one """
    if self.position == len(self.tokens):
      return None
    result = self.tokens[self.position]
    self.position += 1
    return result

  def peek(self):
    """ Return the current token """
    if self.position == len(self.tokens):
      return None
    return self.tokens[self.position]

def read_str(data):
  """ Takes string input and returns an abstract syntax tree """
  tokens = tokenize(data)
  if len(tokens) == 0:
    raise BlankLine("Blank line")
  try:
    return read_form(Reader(tokens))
  except SyntaxError as error:
    print(error)

def tokenize(data):
  """ Breaks the input string apart into tokens """
  return re.findall(token_pattern, data)

def read_form(reader):
  """ Parses a sequence of tokens according to the language's syntax, and returns the resulting abstract syntax tree """
  while True:
    token = reader.peek()
    if token[0] == ';':
      reader.next()
      continue
    elif token == '(':
      return read_list(reader)
    elif token == '[':
      return read_vector(reader)
    elif token == '{':
      return read_map(reader)
    elif token == '\'':
      reader.next()
      return List([Symbol('quote'), read_form(reader)])
    elif token == '`':
      reader.next()
      return List([Symbol('quasiquote'), read_form(reader)])
    elif token == '~':
      reader.next()
      return List([Symbol('unquote'), read_form(reader)])
    elif token == '~@':
      reader.next()
      return List([Symbol('splice-unquote'), read_form(reader)])
    elif token == '@':
      reader.next()
      return List([Symbol('deref'), read_form(reader)])
    elif token == '^':
      reader.next()
      form1 = read_form(reader)
      form2 = read_form(reader)
      return List([Symbol('with-meta'), form2, form1])
    else:
      return read_atom(reader)

def read_atom(reader):
  """ Figures out what kind of an atomic value is represented by a string token """
  atom = reader.next()
  try:
    return int(atom)
  except (TypeError, ValueError) as err:
    try:
      return float(atom)
    except (TypeError, ValueError) as err:
      if atom in unique_values:
        return unique_values[atom]
      try:
        return parse_str(atom)
      except ValueError as err:
        if atom[0] == '"':
          raise SyntaxError("Expected \", got EOF.")
        try:
          return Keyword(atom)
        except ValueError as err:
          try:
            return Symbol(atom)
          except ValueError as err:
            raise SyntaxError("Error parsing or unexpected EOF.")

# The following three methods deal with parsing sequences. Notice the call to read_form on each token. This is what enables sequences to be nested inside each other. It's what puts the "tree" in abstract syntax tree.

def read_list(reader):
  """ Consume tokens from the reader and generate a List """
  result = List()
  reader.next() # drop the opening paranthesis
  while reader.peek() != ")":
    if reader.peek() is None:
      raise SyntaxError("Unexpected EOF while parsing.")
    result.append(read_form(reader))
  reader.next() # drop the closing paranthesis
  return result

def read_vector(reader):
  """ Consume tokens from the reader and generate a Vector """
  result = Vector()
  reader.next() # drop the opening square bracket
  while reader.peek() != "]":
    if reader.peek() is None:
      raise SyntaxError("Unexpected EOF while parsing.")
    result.append(read_form(reader))
  reader.next() # drop the closing square bracket
  return result

def read_map(reader):
  """ Consume tokens from the reader and generate a Vector """
  result = Map()
  reader.next() # drop the opening curly brace
  while reader.peek() != "}":
    if reader.peek() is None:
      raise SyntaxError("Unexpected EOF while parsing.")
    key = read_form(reader)
    value = read_form(reader)
    if value == '}' or value is None:
      raise SyntaxError("Error parsing map literal.")
    result[key] = value
  reader.next() # drop the closing curly brace
  return result