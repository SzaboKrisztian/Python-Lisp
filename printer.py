from lisp_types import *

def escape(strg):
  """ When printing readably, a few special characters need to be escaped. """
  return strg.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"')

def pr_str(ast, print_readably=True):
  """ Takes an abstract syntax tree and returns a printable string """
  if callable(ast) or isinstance(ast, Procedure):
    return "#<function>"
  elif isinstance(ast, List):
    return f"({' '.join([pr_str(x, print_readably) for x in ast])})"
  elif isinstance(ast, Vector):
    return f"[{' '.join([pr_str(x, print_readably) for x in ast])}]"
  elif isinstance(ast, Map):
    return f"{{{' '.join([f'{pr_str(x, print_readably)} {pr_str(y, print_readably)}' for x, y in ast.items()])}}}"
  elif isinstance(ast, SForm):
    return str(ast)
  elif isinstance(ast, bool):
    return "true" if ast else "false"
  elif isinstance(ast, str):
    if print_readably:
      return f'"{escape(ast)}"'
    else:
      return ast
  else:
    return str(ast)