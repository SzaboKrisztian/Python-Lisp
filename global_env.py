from lisp_types import *
import printer, reader
from math import sqrt, floor

""" This file represents the standard functions available in the language """

def func_pr_str(*args):
  if args:
    return ' '.join([printer.pr_str(elem, True) for elem in args])
  else:
    return ""

def func_str(*args):
  if args:
    return ''.join([printer.pr_str(elem, False) for elem in args])
  else:
    return ""

def func_prn(*args):
  if args:
    print(' '.join([printer.pr_str(elem, True) for elem in args]))
  else:
    print()
  return Nil()

def func_println(*args):
  if args:
    print(' '.join([printer.pr_str(elem, False) for elem in args]))
  else:
    print()
  return Nil()

def deref(atom):
  if isinstance(atom, Atom):
    return atom.value
  else:
    raise TypeError('Cannot dereferrence because argument is not an atom.')

def reset(atom, value):
  atom.value = value
  return value

def swap(atom, func, *args):
  atom.value = func(atom.value, *args)
  return atom.value

funcs = {
  Symbol('+'): lambda a, b: a + b,
  Symbol('-'): lambda a, b: a - b,
  Symbol('*'): lambda a, b: a * b,
  Symbol('/'): lambda a, b: a / b,
  Symbol('%'): lambda a, b: a % b,
  Symbol('='): lambda a, b: a == b,
  Symbol('<'): lambda a, b: a < b,
  Symbol('<='): lambda a, b: a <= b,
  Symbol('>'): lambda a, b: a > b,
  Symbol('>='): lambda a, b: a >= b,
  Symbol('sqrt'): lambda a: sqrt(a),
  Symbol('floor'): lambda a: floor(a),
  Symbol('not'): lambda a: (a is False or a == Nil()),
  Symbol('and'): lambda a, b: a and b,
  Symbol('or'): lambda a, b: a or b,
  Symbol('list'): lambda *n: List(n),
  Symbol('vector'): lambda *n: Vector(n),
  Symbol('list?'): lambda n: isinstance(n, List),
  Symbol('vector?'): lambda n: isinstance(n, Vector),
  Symbol('empty?'): lambda n: len(n) == 0,
  Symbol('count'): lambda n: len(n),
  Symbol('pr-str'): func_pr_str,
  Symbol('str'): func_str,
  Symbol('prn'): func_prn,
  Symbol('println'): func_println,
  Symbol('read-string'): reader.read_str,
  Symbol('slurp'): lambda file: open(file, 'r', encoding='UTF-8').read(),
  Symbol('atom'): lambda n: Atom(n),
  Symbol('atom?'): lambda n: isinstance(n, Atom),
  Symbol('deref'): deref,
  Symbol('reset!'): reset,
  Symbol('swap!'): swap,
  Symbol('cons'): lambda el, lst: List([el, *lst]),
  Symbol('concat'): lambda *lsts: List([el for lst in lsts for el in lst]),
  Symbol('nth'): lambda coll, index: coll[index],
  Symbol('first'): lambda coll: Nil() if isinstance(coll, Nil) or len(coll) == 0 else coll[0],
  Symbol('rest'): lambda coll: List() if isinstance(coll, Nil) or len(coll) == 0 else List(coll[1:]),
  Symbol('take'): lambda coll, index: coll[:index]
}