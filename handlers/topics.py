from models.topic import Topic
from handlers.base import BaseHandler
from google.appengine.api import users
from models.comment import Comment
from utils.decorators import validate_csrf, logged_in
from models.topic_subscription import Subscription


class TopicAdd(BaseHandler):
    def get(self):
        return self.render_template("topic_add.html")

    @logged_in
    @validate_csrf
    def post(self):
        title = self.request.get("title")
        text = self.request.get("text")
        user = users.get_current_user()
        new_topic = Topic.create(title, text, user)

        return self.redirect_to("topic-details", topic_id=new_topic.key.id())


class TopicDetails(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        user = users.get_current_user()
        comments = Comment.query(Comment.deleted == False,
                                 Comment.topic_id == topic.key.id()).order(Comment.created).fetch()
        return self.render_template("topic_details.html", {"topic": topic, "comments": comments, "user": user})


class TopicDelete(BaseHandler):
    @validate_csrf
    @logged_in
    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))

        user = users.get_current_user()

        if topic.author_email == user.email() or users.is_current_user_admin():
            topic.delete(topic)

        return self.redirect_to("main-page")


class TopicEdit(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        return self.render_template("topic_edit.html", {"topic": topic})

    @logged_in
    @validate_csrf
    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        new_title = self.request.get("title")
        new_content = self.request.get("text")
        topic.edit(topic, new_title, new_content)
        return self.redirect_to("topic-details", topic_id=topic.key.id())


class TopicSubscribe(BaseHandler):
    def get(self, topic_id):
        # user can subscribe to the topic
        topic = Topic.get_by_id(int(topic_id))
        return self.render_template("topic_details.html", {"topic": topic})

    def post(self, topic_id):
        user = users.get_current_user()
        topic = Topic.get_by_id(int(topic_id))
        if user:
            subscription = Subscription(user_email=user.email(), topic_title=topic.title, topic_id=int(topic_id))
            subscription.put()

        return self.redirect_to("topic-details", topic_id=topic.key.id())


class TopicUnsubscribe(BaseHandler):
    def post(self, subscription_id):
        subscription = Subscription.get_by_id(int(subscription_id))
        subscription.deleted = True
        subscription.put()
        self.redirect_to("topic-details", topic_id=subscription.topic_id)
