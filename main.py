import webapp2
from handlers.base import MainHandler, CookieAlertHandler
from handlers.topics import TopicAdd, TopicDetails, TopicDelete, TopicEdit, TopicSubscribe, TopicUnsubscribe
from handlers.comment import CommentAdd, CommentDelete, CommentsUser
from workers.email_new_comment import EmailNewCommentWorker, EmailTopicSubscriberWorker
from handlers.topic_subscription import Subscriptions
from crons.delete_topics import DeleteTopicsCron
from crons.delete_comments import DeleteCommentsCron
from handlers.forum_subscriptions import ForumSubscribe, ForumUnsubscribe
from crons.email_subscriber import EmailSubscriberCron
from handlers.gallery import GalleryHandler

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieAlertHandler, name="set-cookie"),
    webapp2.Route('/topic/add', TopicAdd),
    webapp2.Route('/topic/<topic_id:\d+>/details', TopicDetails, name="topic-details"),
    webapp2.Route('/topic/<topic_id:\d+>/comment-add', CommentAdd),
    webapp2.Route('/task/email-new-comment', EmailNewCommentWorker),
    webapp2.Route('/task/email-topic-subscriber', EmailTopicSubscriberWorker),
    webapp2.Route('/topic/<topic_id:\d+>/delete', TopicDelete),
    webapp2.Route('/topic/<topic_id:\d+>/edit', TopicEdit),
    webapp2.Route('/comment/<comment_id:\d+>/delete', CommentDelete),
    webapp2.Route('/comment/user', CommentsUser),
    webapp2.Route('/topic/<topic_id:\d+>/subscribe', TopicSubscribe),
    webapp2.Route('/<subscription_id:\d+>/unsubscribe', TopicUnsubscribe),
    webapp2.Route('/subscriptions/user', Subscriptions, name="subscriptions"),
    webapp2.Route("/user/unsubscribe", ForumUnsubscribe),
    webapp2.Route("/cron/email-subscriber", EmailSubscriberCron),
    webapp2.Route("/cron/delete-topics", DeleteTopicsCron, name="cron-delete-topics"),
    webapp2.Route("/cron/delete-comments", DeleteCommentsCron),
    webapp2.Route("/user/subscribe", ForumSubscribe),
    webapp2.Route('/gallery', GalleryHandler, name="gallery"),
], debug=True)
