from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Post.models import Post
from User.controller.UserController import UserController
from .controller.PostController import PostController

import json


# Create your views here.
@csrf_exempt
def create_post(request):
    """
    Handles the endpoint '/post/create/'
    parameters are received from the request body
    the params are
    title : str [The title of the post]
    content : str [The content of the post]
    author : str [The email of the author of the post]

    returns the created post if creation is successful
    else an error message as HttpResponse
    """
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    title = body.get('title', '')
    content = body.get('content', '')
    authorEmail = body.get('author', '')

    if not title or not content or not authorEmail:
        return HttpResponse('Invalid data, Missing Fields')

    author = UserController(authorEmail)
    if not author.userExists:
        return HttpResponse('User does not exist')

    newPost = Post(title=title, content=content, author=author.user)
    newPost.save()
    return HttpResponse(PostController.serializePost(newPost), content_type='application/json')


@csrf_exempt
def fetch_all_posts(request):
    """
    Handles the endpoint '/post/all/'

    Returns a list of all serialized posts as json
    """
    allPosts = Post.objects.all()
    postsList = [PostController.toDict(post) for post in allPosts]
    return HttpResponse(json.dumps(postsList), content_type='application/json')