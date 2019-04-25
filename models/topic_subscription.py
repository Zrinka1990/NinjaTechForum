from google.appengine.ext import ndb


class Subscription(ndb.Model):
    user_email = ndb.StringProperty()
    topic_id = ndb.IntegerProperty()
    topic_title = ndb.StringProperty()
    deleted = ndb.BooleanProperty(default=False)
    