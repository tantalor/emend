from emend import Site

def get(handler, response):
  response.sites = Site.all()
