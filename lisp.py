import readline, reader, printer, evaluator, environment, sys
from lisp_types import *

def READ(inpt):
  """ Read source code as a string and return an abstract syntax tree """
  try:
    return reader.read_str(inpt)
  except Exception as error:
    print(error)

def EVAL(ast, env):
  """ Evaluate an abstract syntax tree in an environment """
  return evaluator.evaluate(ast, env)

def PRINT(ast):
  """ Return a string output of an abstract syntax tree """
  return printer.pr_str(ast)

def rep(inpt, env):
  """ Read, evaluate, and print """
  return PRINT(EVAL(READ(inpt), env))

# Instantiate the global environment and define some symbols

global_env = environment.Environment(is_global=True)
global_env.define(Symbol('eval'), lambda ast: evaluator.evaluate(ast, global_env))
global_env.define(Symbol('*ARGV*'), List(sys.argv[2:]))

# The following forms are defined using Lisp itself

rep('(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f) "\nnil)")))))', global_env)
rep('(defmacro! cond (fn* (& xs) (if (> (count xs) 0) (list \'if (first xs) (if (> (count xs) 1) (nth xs 1) (throw "odd number of forms to cond")) (cons \'cond (rest (rest xs)))))))', global_env)

# If the script is run with command line arguments, interpret the first argument as a source code file to execute, and save the rest as a list under the global *ARGV* symbol. At the end of execution, quit.

if (len(sys.argv) >= 2):
  rep(f'(load-file "{sys.argv[1]}")', global_env)
  sys.exit(0)

# Otherwise start the REPL environment

while True:
  try:
    inpt = input('lisp> ')
    print(rep(inpt, global_env))
  except BlankLine:
    continue
  except EOFError:
    break
  except Exception as error:
    print(error)
