import datetime
from handlers.base import BaseHandler
from models.comment import Comment


class DeleteCommentsCron(BaseHandler):
    def get(self):
        # delete comments from database whose deleted property was set to True 30 days ago or more
        deleted_comments = Comment.query(Comment.deleted == True,
                                         Comment.updated < datetime.datetime.now() - datetime.timedelta(days=30)).fetch()

        for comment in deleted_comments:
            comment.key.delete()
