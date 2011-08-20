from google.appengine.ext import db


class MockModel(db.Model):
  def put(self):
    pass
  def delete(self):
    pass
