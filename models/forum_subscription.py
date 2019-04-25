from google.appengine.ext import ndb


class Subscription(ndb.Model):
    user_email = ndb.StringProperty()
