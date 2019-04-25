from models.comment import Comment
from handlers.base import BaseHandler
from google.appengine.api import users
from models.topic import Topic
from utils.decorators import validate_csrf, logged_in


class CommentAdd(BaseHandler):
    @logged_in
    @validate_csrf
    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        content = self.request.get("text")
        user = users.get_current_user()
        Comment.create(content, user, topic)
        return self.redirect_to("topic-details", topic_id=topic.key.id())


class CommentDelete(BaseHandler):
    def post(self, comment_id):
        comment = Comment.get_by_id(int(comment_id))
        comment.delete(comment)
        return self.redirect_to("topic-details", topic_id=comment.topic_id)


class CommentsUser(BaseHandler):
    # user can se a list of all his/her comments
    @logged_in
    def get(self):
        user = users.get_current_user()
        comments = Comment.query(Comment.author_email == user.email()).order(-Comment.created).fetch()
        return self.render_template("comments_user.html", {"comments": comments})
