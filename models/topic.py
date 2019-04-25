from google.appengine.ext import ndb
from google.appengine.api import taskqueue
from models.forum_subscription import Subscription


class Topic(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    author_email = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def create(cls, title, content, user):
        topic = cls(title=title, content=content, author_email=user.email())
        topic.put()

        # run background task to send email to topic subscriber about new topics
        taskqueue.add(url='/cron/email-subscriber')

        return topic

    @classmethod
    def delete(cls, topic):
        topic.deleted = True
        topic.put()

        return topic

    @classmethod
    def edit(cls, topic, new_title, new_content):
        topic.title = new_title
        topic.content = new_content
        topic.put()

        return topic
