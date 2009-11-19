import os

def is_dev():
  return 'SERVER_SOFTWARE' not in os.environ\
    or 'Development' in os.environ['SERVER_SOFTWARE']

def branch(choices):
  """Choose one of the choices based on the environment."""
  if choices:
    if is_dev() and 'dev' in choices:
      return choices['dev']
    elif 'prod' in choices:
      return choices['prod']
    else:
      return choices
