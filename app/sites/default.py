from model.site import Site
PAGE_SIZE = 10

def get(handler, response):
  # get some sites
  from_domain = handler.request.get('from')
  if from_domain:
    from_site = Site.all().\
      filter('domain =', from_domain).get()
    sites = Site.all().\
      filter('open =', from_site.open).\
      filter('domain >=', from_domain).\
      order('domain').\
      fetch(PAGE_SIZE+1)
    if len(sites) < PAGE_SIZE+1:     
      sites += Site.all().\
        filter('open <', from_site.open).\
        order('-open').\
        order('domain').\
        fetch(PAGE_SIZE+1-len(sites))
  else:
    sites = Site.all().\
      order('-open').\
      order('domain').\
      fetch(PAGE_SIZE+1)
  # for output
  response.sites = sites[:PAGE_SIZE]
  
  if len(sites) > PAGE_SIZE:
    response.has_next = 1
    response.next_from = sites[PAGE_SIZE].domain
