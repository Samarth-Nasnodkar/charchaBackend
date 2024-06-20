import json

from ..models import Post
import uuid
from typing import Optional
from User.controller.UserController import UserController


class PostController:
    def __init__(self, _id: uuid):
        self.id = _id
        self.post = None
        self.initPost()

    def initPost(self):
        dbPost = Post.objects.filter(pk=self.id)
        if dbPost.exists():
            self.post = dbPost.first()

    @property
    def postExists(self) -> bool:
        return self.post is not None

    @staticmethod
    def createPost(title: str, content: str, author: str) -> Post:
        newPost = Post(title=title, content=content, author=author)
        newPost.save()
        return newPost

    def deletePost(self):
        if self.postExists:
            self.post.delete()

    def updatePostField(self, field: str, value) -> bool:
        if not self.postExists:
            return False

        if field == 'title':
            self.post.title = value
        elif field == 'content':
            self.post.content = value
        return False

    def updatePost(self, update: dict) -> Optional[Post]:
        if not self.postExists:
            return None

        for key, value in update.items():
            res = self.updatePostField(key, value)
            if not res:
                return None

        self.post.save()
        return self.post

    @staticmethod
    def toDict(post: Post) -> dict:
        return {
            'title': post.title,
            'content': post.content,
            'author': UserController.toDict(post.author)
        }

    @staticmethod
    def serializePost(post: Post):
        postDict = PostController.toDict(post)
        return json.dumps(postDict)
