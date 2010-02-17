from emend import Site
PAGE_SIZE = 10

def get(handler, response):
  # get some sites
  from_domain = handler.request.get('from')
  from_key_name = Site.key_name_from_domain(from_domain)
  from_site = Site.get_by_key_name(from_key_name)
  if from_site:
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
