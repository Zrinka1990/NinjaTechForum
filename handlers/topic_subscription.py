from models.topic_subscription import Subscription
from google.appengine.api import users
from handlers.base import BaseHandler


class Subscriptions(BaseHandler):
    def get(self):
        # user can subscribe to the topic
        user = users.get_current_user()
        if user:
            subscriptions = Subscription.query(Subscription.user_email == user.email(),
                                               Subscription.deleted == False).order(Subscription.topic_title).fetch()
            return self.render_template("subscriptions.html", {"subscriptions": subscriptions})
        return self.write("You must be logged in to see subscribed topics")
