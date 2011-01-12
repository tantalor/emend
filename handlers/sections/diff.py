def get(handler, response):
  response.dst = handler.request.get('dst')
  response.src = handler.request.get('src')
