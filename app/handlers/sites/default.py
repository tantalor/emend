from emend import Site
PAGE_SIZE = 1

def get(handler, response):
  from_domain = handler.request.get('from')
  to_domain = handler.request.get('to')
  
  from_site, to_site = None, None
  
  if to_domain:
    to_key_name = Site.key_name_from_domain(to_domain)
    to_site = Site.get_by_key_name(to_key_name)
  
  if from_domain:
    from_key_name = Site.key_name_from_domain(from_domain)
    from_site = Site.get_by_key_name(from_key_name)
  
  # fetch sites
  if to_site:
    sites = Site.all().\
      filter('open =', to_site.open).\
      filter('domain <=', to_site.domain).\
      order('-domain').\
      fetch(PAGE_SIZE+2)
    sites.reverse()
    if len(sites) < PAGE_SIZE+2:
      pad = Site.all().\
        filter('open >', to_site.open).\
        order('open').\
        order('-domain').\
        fetch(PAGE_SIZE+2-len(sites))
      pad.reverse()
      sites = pad+sites
    if len(sites) > PAGE_SIZE+1:
      response.sites = sites[1:PAGE_SIZE+1]
    else:
      response.sites = sites[:PAGE_SIZE]
  elif from_site:
    sites = Site.all().\
      filter('open =', from_site.open).\
      filter('domain >=', from_site.domain).\
      order('domain').\
      fetch(PAGE_SIZE+1)
    if len(sites) < PAGE_SIZE+1:     
      sites += Site.all().\
        filter('open <', from_site.open).\
        order('-open').\
        order('domain').\
        fetch(PAGE_SIZE+1-len(sites))
    response.sites = sites[:PAGE_SIZE]
  else:
    sites = Site.all().\
      order('-open').\
      order('domain').\
      fetch(PAGE_SIZE+1)
    response.sites = sites[:PAGE_SIZE]
  
  # pagination
  if to_site:
    response.next.url = "%s?from=%s" % (handler.base_path(), to_site.domain)
    
    if len(sites) > PAGE_SIZE+1:
      response.previous.url = "%s?to=%s" % (handler.base_path(), sites[1].domain)
  else:
    if from_site:
      response.previous.url = "%s?to=%s" % (handler.base_path(), from_site.domain)
  
    if len(sites) > PAGE_SIZE:
      response.next.url = "%s?from=%s" % (handler.base_path(), sites[PAGE_SIZE].domain)
