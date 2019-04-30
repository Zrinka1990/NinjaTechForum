from handlers.base import BaseHandler
from google.appengine.api import mail
from models.topic_subscription import Subscription


class EmailNewCommentWorker(BaseHandler):
    def post(self):
        topic_author_email = self.request.get("topic_author_email")
        topic_title = self.request.get("topic_title")
        topic_id = self.request.get("topic_id")
        mail.send_mail(sender="zrinka.000a@gmail.com",
                       to=topic_author_email,  # receiver is the person who created the topic
                       subject="New comment on your topic",
                       body="hello",
                       html="""\
                            <html>
                              <body>
                                   <p>
                                   Your topic "{0}" received a new comment. Click on
                                   <a href="http://ninjatechforum2-239216.appspot.com/topic/{1}/details">
                                   this link</a> to see it. 
                                   </p> 
                              </body>
                            </html>""".format(topic_title, topic_id))


class EmailTopicSubscriberWorker(BaseHandler):
    def post(self):
        topic_title = self.request.get("topic_title")
        topic_id = self.request.get("topic_id")
        subscriptions = Subscription.query(Subscription.topic_id == int(topic_id), Subscription.deleted == False).fetch()

        for subscription in subscriptions:
            topic_subscriber_email = subscription.user_email
            mail.send_mail(sender="zrinka.000a@gmail.com",
                           to=topic_subscriber_email,
                           # receiver is the person who created the topic
                           subject="New comment on subscribed topic",
                           body="hello",
                           html="""\
                               <html>
                                 <body>
                                      <p>
                                      The topic "{0}" you are subscribed to received a new comment. Click on
                                      <a href="http://ninjatechforum2-239216.appspot.com/topic/{1}/details">
                                      this link</a> to see it!
                                      </p>
                                 </body>
                               </html>""".format(topic_title, topic_id))
