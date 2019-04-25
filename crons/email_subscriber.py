import datetime
from handlers.base import BaseHandler
from handlers.topics import Topic
from google.appengine.api import mail
from models.forum_subscription import Subscription


class EmailSubscriberCron(BaseHandler):
    def get(self):
        # get topics which are created or updated in last 24 hours
        hottest_topics = Topic.query(Topic.deleted == False, Topic.created > datetime.datetime.now() -
                                     datetime.timedelta(hours=24)).fetch()

        forum_subscriptions = Subscription.query().fetch()

        body_content = "New topics in last 24 hours"

        for topic in hottest_topics:
            body_content += """{0}: 
                Click oh this link to see it: http://ninjatechforum-237615.appspot.com/topic/{1}/details
                 '\n'""".format(topic.title, topic.key.id())

        emails = []

        for subscription in forum_subscriptions:
            emails.append(subscription.user_email)
            subscriber_email = subscription.user_email
            mail.send_mail(sender="zrinka.000a@gmail.com",
                           to=subscriber_email,
                           subject="Hottest topics",
                           body=body_content)
