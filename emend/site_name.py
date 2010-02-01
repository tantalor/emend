from megaera import local

def site_name():
  try:
    return 'Emend: %s' % local.config_get('tagline')
  except KeyError:
    return 'Emend'
