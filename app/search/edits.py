from model.edit import Edit

def get(handler, response):
  query = handler.request.get('q')
  response.query = query
  response.edits = list(Edit.all().search(query))
