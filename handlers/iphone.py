from emend.bookmarklet import bookmarklet

def get(handler, response):
  response.update(bookmarklet=bookmarklet())
