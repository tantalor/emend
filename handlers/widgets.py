def get(handler, response):
  response.edit_widget = ''.join(file('local-static/html/widgets/edit.html').readlines()).rstrip()
