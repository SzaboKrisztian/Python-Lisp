from lisp_types import *
from environment import Environment as Env

""" This file contains the heart of the interpreter. It is concerned with parsing an abstract syntax tree, and evaluate it until it can be evaluated no further (usually arriving at a single value) """

# The special forms are language constructs that control execution flow, modify the environment, declare functions, and deal with macros.
special_forms = [Symbol('def!'), Symbol('let*'), Symbol('do'), Symbol('if'), Symbol('fn*'), Symbol('quote'), Symbol('quasiquote'), Symbol('defmacro!'), Symbol('macroexpand')]

# A quick explanation of tail call optimization: the evaluate function contains an infinite loop. This allows optimizing function calls that are tail recursive (they call themselves as the last statement of the function). This is achieved by setting the ast to whatever needs to be evaluated next, change the environment if needed, and then continuing from the top of the loop for another cycle of evaluation. This allows writing smarter and more performant recursive functions that avoid overflowing the call stack in the case of deep recursion.
def evaluate(ast, env):
  """ Evaluates an abstract syntax tree in a given environment """
  while True: # Infinite loop used for tail call optimization
    # First check if the AST is a macro, and if so expand it.
    ast = macroexpand(ast, env)

    # If the ast is not a list, call the mutually recursive eval_ast() function on it.
    if not isinstance(ast, List):
      return eval_ast(ast, env)

    # Return the AST as it is, if it's just an empty sequence, as there's nothing more to be done.
    if len(ast) == 0:
      return ast
    elif not isinstance(ast[0], List) and ast[0] in special_forms:

      # This following section deals with applying the logic of each special form.
      form, args = ast[0], ast[1:]

      # def! assigns a value to a key in the current environment.
      if form == Symbol("def!"):
        value = evaluate(args[1], env)
        env.define(args[0], value)
        return value

      # let* evaluates a form in a temporary environment.
      elif form == Symbol("let*"):  
        var_list = args[0]
        if isinstance(var_list, (List, Vector)) and len(var_list) % 2 == 0:
          new_env = Env(outer=env)
          for i in range(0, len(var_list), 2):
            new_env.define(var_list[i], evaluate(var_list[i + 1], new_env))
          env = new_env
          ast = args[1]
          continue # Tail call optimization
        else:
          raise SyntaxError("Invalid argument list supplied.")

      # do evaluates all the elements of the list, and returns the final evaluated one. This constructs provides a way to sequentially execute things.
      elif form == Symbol("do"):
        for expr in args[:-1]:
          last = evaluate(expr, env)
        ast = args[-1]
        continue # Tail call optimization

      # if works as you'd expect. To be noted that it only evaluates the needed argument (first argument if the condition is true, second otherwise), and is also tail call optimized.
      elif form == Symbol("if"):
        cond, true = args[0], args[1]
        false = args[2] if len(args) > 2 else None
        ev = evaluate(cond, env)
        if ev is False or ev == Nil():
          if false is not None:
            ast = false
            continue
          else:
            return Nil()
        else:
          ast = true
          continue

      # fn* defines a lambda function, with the first argument being the parameter list, and the second being the function's body.
      elif form == Symbol("fn*"):
        params, body = args[0], args[1]

        def fn(*arguments):
          return evaluate(body, Env(env, params, arguments))
        
        return Procedure(body, params, env, fn)

      # quote defers evaluation, just returning its argument as it is.
      elif form == Symbol('quote'):
        return args[0]

      # quasiquote enables a quoted list to have certain elements evaluted by the way of unquote and splice-unquote.
      elif form == Symbol('quasiquote'):
        ast = quasiquote(args[0])
        continue # Tail call optimized

      # defmacro! defines a new macro in the current environment.
      elif form == Symbol("defmacro!"):
        value = evaluate(args[1], env)
        value.is_macro = True
        env.define(args[0], value)
        return value

      # macroexpand allows explicitly calling the macroexpand function. This can aid in debugging macros.
      elif form == Symbol("macroexpand"):
        return macroexpand(args[0], env)

      # End of special forms logic

    else:
      # First evaluate the list that holds the AST
      evaluated = eval_ast(ast, env)

      # Procedures primarily represent user defined functions
      if isinstance(evaluated[0], Procedure):
        proc = evaluated[0]
        ast = proc.ast
        env = proc.make_env(Env, evaluated[1:])
        continue # Tail call optimization

      # Callables represent the built-in functions or fully evaluated procedures
      elif callable(evaluated[0]):
        return evaluated[0](*evaluated[1:])

      # During evaluation, a Lisp list is expected to hold a function reference as its first element
      else:
        raise SyntaxError("First element of list is not a function.")
      

def eval_ast(ast, env):
  """ Function that is mutually recursive with evaluate(), thus enabling the actual evaluation of an abstract syntax tree (which is a nested data structure) """
  if isinstance(ast, Symbol):
    # If dealing with a Symbol, get its associated value from the environment
    return env.get(ast)
  # If dealing with a sequence type, return a new one of the same type, but with its values evaluated
  elif isinstance(ast, List):
    return List([evaluate(elem, env) for elem in ast])
  elif isinstance(ast, Vector):
    return Vector([evaluate(elem, env) for elem in ast])
  elif isinstance(ast, Map):
    return Map({key:evaluate(value, env) for key, value in ast.items()})
  else:
    # In all other cases (atomic values mostly), nothing more can be evaluated, so just return it
    return ast

# Helper functions for evaluate()

def is_non_empty_seq(ast):
  """ Check whether AST is a sequence with at least an element """
  return isinstance(ast, (List, Vector)) and len(ast) > 0

def quasiquote(ast):
  """ Processes a quasiquoted AST """
  # If 
  if not is_non_empty_seq(ast):
    return List([Symbol('quote'), ast])
  elif ast[0] == Symbol('unquote'):
    return ast[1]
  elif is_non_empty_seq(ast[0]) and ast[0][0] == Symbol('splice-unquote'):
    return List([Symbol('concat'), ast[0][1], quasiquote(ast[1:])])
  else:
    return List([Symbol('cons'), quasiquote(ast[0]), quasiquote(ast[1:])])

def is_macro_call(ast, env):
  """ Check if a procedure of callable is flagged as being a macro """
  if not isinstance(ast, List):
    return False
  if len(ast) == 0 or not isinstance(ast[0], Symbol):
    return False
  try:
    func = env.get(ast[0])
  except ValueError:
    return False
  if (isinstance(func, Procedure) or callable(func)) and hasattr(func, 'is_macro'):
    return func.is_macro
  else:
    return False

def macroexpand(ast, env):
  """ Expands a macro until it results in an AST that can be directly evaluated """
  while is_macro_call(ast, env):
    func = env.get(ast[0])
    ast = func(*ast[1:])
  return ast