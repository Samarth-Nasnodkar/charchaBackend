from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid

from Comment.controller.CommentController import CommentController
from User.controller.UserController import UserController
from Post.controller.PostController import PostController
from .controller.CommentController import CommentController, Comment


# Create your views here.
@csrf_exempt
def createComment(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    content = body.get('content', None)
    authorUsername = body.get('author', None)
    postId = body.get('post', None)
    if content is None or authorUsername is None or postId is None:
        return HttpResponse('Invalid Request')

    postId = uuid.UUID(postId)

    author = UserController(username=authorUsername)
    if not author.userExists:
        return HttpResponse('Invalid User')

    post = PostController(postId)
    if not post.postExists:
        return HttpResponse('Invalid Post')

    comment = CommentController.createComment(content, author.user, post.post)
    return HttpResponse(CommentController.serializeComment(comment), content_type='application/json')


@csrf_exempt
def fetchAllComments(request):
    commentsList = CommentController.fetchAllComments()
    dictList = [CommentController.toDict(comment) for comment in commentsList]
    return HttpResponse(json.dumps(dictList), content_type='application/json')


@csrf_exempt
def fetchCommentsByPost(request, post_id):
    post_id = uuid.UUID(post_id)
    dbComments = Comment.objects.filter(post_id=post_id).all()
    dbCommentsList = [CommentController.toDict(comment) for comment in dbComments]
    return HttpResponse(json.dumps(dbCommentsList), content_type='application/json')


@csrf_exempt
def fetchCommentsByAuthor(request, author_username):
    dbComments = Comment.objects.filter(author__username=author_username)
    dbCommentsList = [CommentController.toDict(comment) for comment in dbComments]
    return HttpResponse(json.dumps(dbCommentsList), content_type='application/json')