from django.shortcuts import render, HttpResponse
from .controller.AuthController import AuthController
from User.controller.UserController import UserController
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
@csrf_exempt
def register_user(request):
    """
    Handles the endpoint '/auth/register'

    parameters are received from the request body
    the params are
    username : str [The username of the user]
    email : str [The email of the user]
    password : str [The password of the user]
    profile_picture_url : str [The profile picture url of the user]

    returns the created user if creation is successful
    else an error message as HttpResponse
    """
    # loading the request body
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    # getting values of the necessary fields
    username = body.get('username', '')
    email = body.get('email', '')
    password = body.get('password', '')
    profile_picture_url = body.get('profile_picture_url', '')

    # Setting a default value to profile picture if None
    if profile_picture_url == '':
        profile_picture_url = 'https://api.dicebear.com/9.x/micah/svg?seed=' + username

    res = AuthController.register(username, email, password, profile_picture_url)

    # Handling error
    if res is None:
        return HttpResponse('User already exists')

    # Returning the created user as JSON
    return HttpResponse(UserController.serialize(res), content_type='application/json')


@csrf_exempt
def login_user(request):
    """
    Handles the endpoint '/auth/login'

    parameters are received from the request body
    the params are
    email : str [The email of the user]
    password : str [The password of the user]

    returns the user if login is successful
    else an error message as HttpResponse
    """

    # loading the request body
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    # getting the values of the necessary fields
    email = body.get('email', '')
    password = body.get('password', '')

    loggedUser = AuthController.login(email, password)

    # Handling error in case of unsuccessful login
    if loggedUser is None:
        return HttpResponse('Invalid login details')

    # Returning the logged-in user as JSON
    return HttpResponse(UserController.serialize(loggedUser), content_type='application/json')
