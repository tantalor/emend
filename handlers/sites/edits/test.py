def post(handler, response):
  edit = handler.get_edit(required=True)
  response.status = edit.test()
