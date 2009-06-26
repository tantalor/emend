import re

def bookmarklet():
  bookmarklet = ''.join(file('js/bookmarklet.js').readlines())
  bookmarklet = re.compile('\s').sub('', bookmarklet)
  return bookmarklet
