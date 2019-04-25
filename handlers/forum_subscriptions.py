from handlers.base import BaseHandler
from google.appengine.api import users
from models.forum_subscription import Subscription
from utils.decorators import logged_in, validate_csrf


class ForumSubscribe(BaseHandler):
    def get(self):
        return self.render_template("main.html")

    @logged_in
    @validate_csrf
    def post(self):
        user = users.get_current_user()
        subscription = Subscription(user_email=user.email())
        subscription.put()
        return self.redirect_to("main-page")


class ForumUnsubscribe(BaseHandler):
    def get(self):
        return self.render_template("main.html")

    @logged_in
    @validate_csrf
    def post(self):
        user = users.get_current_user()
        subscription = Subscription.query(Subscription.user_email == user.email()).get()
        subscription.key.delete()
        return self.redirect_to("main-page")
