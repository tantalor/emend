import os

def server_software():
  return os.environ.get('SERVER_SOFTWARE')

def is_dev():
  _server_software = server_software()
  return not _server_software or 'Development' in _server_software

def branch(choices):
  """Choose one of the choices based on the environment."""
  if choices:
    if is_dev() and 'dev' in choices:
      return choices['dev']
    elif 'prod' in choices:
      return choices['prod']
    else:
      return choices
