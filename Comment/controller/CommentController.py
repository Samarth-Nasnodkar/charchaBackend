from ..models import Comment
import uuid
from User.controller.UserController import UserController, User
from Post.controller.PostController import PostController, Post

import json


class CommentController:
    def __init__(self, commentId):
        self.comment = None
        self.initComment(commentId)

    def initComment(self, commentId):
        dbComment = Comment.objects.filter(id=commentId)
        if dbComment.exists():
            self.comment = dbComment.first()

    def deleteComment(self) -> bool:
        if self.comment is not None:
            self.comment.delete()
            return True
        return False

    @staticmethod
    def toDict(comment: Comment) -> dict:
        return {
            "id": str(comment.id),
            "content": comment.content,
            "author": UserController.toDict(comment.author),
            "post": PostController.toDict(comment.post),
            "created_at": str(comment.created_at),
        }

    @staticmethod
    def serializeComment(comment: Comment):
        return json.dumps(CommentController.toDict(comment))

    @staticmethod
    def createComment(content: str, author: User, post: Post):
        comment = Comment(content=content, author=author, post=post)
        comment.save()
        return comment

    @staticmethod
    def fetchCommentsByAuthor(author: User):
        dbComments = Comment.objects.filter(author=author)
        return list(dbComments.all())

    @staticmethod
    def fetchCommentsByPost(post: Post):
        dbComments = Comment.objects.filter(post=post)
        return list(dbComments.all())

    @staticmethod
    def fetchAllComments():
        dbComments = Comment.objects.all()
        return list(dbComments)
