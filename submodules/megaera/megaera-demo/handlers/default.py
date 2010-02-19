def get(handler, response):
  name = handler.request.get('name')
  response.messages.hello = "hello %s" % name
