from django.shortcuts import render, HttpResponse
from .controller.AuthController import AuthController
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
@csrf_exempt
def register_user(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    username = body.get('username', '')
    email = body.get('email', '')
    password = body.get('password', '')
    profile_picture_url = body.get('profile_picture_url', '')

    # print(username, email, password, profile_picture_url)
    if profile_picture_url == '':
        profile_picture_url = 'https://api.dicebear.com/9.x/micah/svg?seed=' + username
    res = AuthController.register(username, email, password, profile_picture_url)
    if res is None:
        return HttpResponse('User already exists')
    return HttpResponse(res)


@csrf_exempt
def login_user(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    email = body.get('email', '')
    password = body.get('password', '')

    loggedUser = AuthController.login(email, password)
    if loggedUser is None:
        return HttpResponse('Invalid login details')

    return HttpResponse(loggedUser)
